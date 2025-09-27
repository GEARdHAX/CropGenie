import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:tflite_flutter_helper_plus/tflite_flutter_helper_plus.dart';
import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;

class TFLiteService {
  Interpreter? _interpreter;
  bool _isModelLoaded = false;
  
  // Model configuration
  static const int inputSize = 640; // YOLO input size
  static const int numClasses = 80; // COCO dataset classes
  static const double confidenceThreshold = 0.5;
  static const double nmsThreshold = 0.4;

  Future<bool> loadModel() async {
    try {
      // Load interpreter from assets
      _interpreter = await Interpreter.fromAsset('assets/best_float32.tflite');
      
      // Print model info
      var inputTensors = _interpreter!.getInputTensors();
      var outputTensors = _interpreter!.getOutputTensors();
      
      print('Model loaded successfully');
      print('Input shape: ${inputTensors.first.shape}');
      print('Output shape: ${outputTensors.first.shape}');
      
      _isModelLoaded = true;
      return true;
    } catch (e) {
      print('Error loading model: $e');
      _isModelLoaded = false;
      return false;
    }
  }

  Future<List<Map<String, dynamic>>> runInference(String imagePath) async {
    if (!_isModelLoaded || _interpreter == null) {
      throw Exception('Model not loaded. Call loadModel() first.');
    }

    try {
      // Load image into TensorImage
      var inputImage = TensorImage.fromFile(File(imagePath));

      // Build ImageProcessor to resize and normalize
      final imageProcessor = ImageProcessorBuilder()
          .add(ResizeOp(inputSize, inputSize, ResizeMethod.bilinear))
          .add(NormalizeOp(0, 255)) // [0,255] -> [0,1]
          .build();

      // Apply preprocessing
      inputImage = imageProcessor.process(inputImage);

      // Get input/output shapes
      var inputShape = _interpreter!.getInputTensors().first.shape;
      var outputShape = _interpreter!.getOutputTensors().first.shape;

      // Input buffer
      var inputBuffer = inputImage.buffer;

      // Output buffer
      var outputBuffer = List.filled(outputShape.reduce((a, b) => a * b), 0.0);

      // Run inference
      _interpreter!.run(inputBuffer, outputBuffer);

      // Process YOLO output
      return _processYoloOutput(outputBuffer, outputShape);
    } catch (e) {
      print('Error during inference: $e');
      return [];
    }
  }

  List<Map<String, dynamic>> _processYoloOutput(List<double> output, List<int> outputShape) {
    List<Map<String, dynamic>> detections = [];
    
    // YOLO output format: [batch, 25200, 85] where 85 = 4 (bbox) + 1 (confidence) + 80 (classes)
    int numDetections = outputShape[1]; // 25200
    int numValues = outputShape[2]; // 85
    
    for (int i = 0; i < numDetections; i++) {
      int baseIndex = i * numValues;
      
      // Extract bounding box coordinates (center_x, center_y, width, height)
      double centerX = output[baseIndex];
      double centerY = output[baseIndex + 1];
      double width = output[baseIndex + 2];
      double height = output[baseIndex + 3];
      
      // Extract confidence score
      double confidence = output[baseIndex + 4];
      
      // Skip if confidence is too low
      if (confidence < confidenceThreshold) continue;
      
      // Extract class probabilities
      List<double> classScores = [];
      for (int j = 5; j < numValues; j++) {
        classScores.add(output[baseIndex + j]);
      }
      
      // Find class with highest probability
      int classId = classScores.indexOf(classScores.reduce((a, b) => a > b ? a : b));
      double classScore = classScores[classId];
      
      // Calculate final confidence
      double finalConfidence = confidence * classScore;
      
      if (finalConfidence >= confidenceThreshold) {
        detections.add({
          'classId': classId,
          'className': _getClassName(classId),
          'confidence': finalConfidence,
          'bbox': {
            'x': centerX - width / 2,
            'y': centerY - height / 2,
            'width': width,
            'height': height,
          }
        });
      }
    }
    
    // Apply Non-Maximum Suppression
    return _applyNMS(detections);
  }

  String _getClassName(int classId) {
    // COCO class names (simplified list)
    List<String> classNames = [
      'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
      'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
      'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
      'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
      'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
      'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
      'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
      'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
      'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
      'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
      'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
      'toothbrush'
    ];
    
    return classId < classNames.length ? classNames[classId] : 'unknown';
  }

  List<Map<String, dynamic>> _applyNMS(List<Map<String, dynamic>> detections) {
    // Sort by confidence
    detections.sort((a, b) => b['confidence'].compareTo(a['confidence']));
    
    List<Map<String, dynamic>> filtered = [];
    
    for (var detection in detections) {
      bool shouldKeep = true;
      
      for (var existing in filtered) {
        if (_calculateIoU(detection['bbox'], existing['bbox']) > nmsThreshold) {
          shouldKeep = false;
          break;
        }
      }
      
      if (shouldKeep) {
        filtered.add(detection);
      }
    }
    
    return filtered;
  }

  double _calculateIoU(Map<String, dynamic> bbox1, Map<String, dynamic> bbox2) {
    double x1 = bbox1['x'];
    double y1 = bbox1['y'];
    double w1 = bbox1['width'];
    double h1 = bbox1['height'];
    
    double x2 = bbox2['x'];
    double y2 = bbox2['y'];
    double w2 = bbox2['width'];
    double h2 = bbox2['height'];
    
    double intersectionX = (x1 < x2 + w2 && x1 + w1 > x2) ? 
        (x1 > x2 ? x1 : x2) : 0;
    double intersectionY = (y1 < y2 + h2 && y1 + h1 > y2) ? 
        (y1 > y2 ? y1 : y2) : 0;
    double intersectionW = (x1 < x2 + w2 && x1 + w1 > x2) ? 
        ((x1 + w1 < x2 + w2 ? x1 + w1 : x2 + w2) - intersectionX) : 0;
    double intersectionH = (y1 < y2 + h2 && y1 + h1 > y2) ? 
        ((y1 + h1 < y2 + h2 ? y1 + h1 : y2 + h2) - intersectionY) : 0;
    
    double intersection = intersectionW * intersectionH;
    double union = w1 * h1 + w2 * h2 - intersection;
    
    return union > 0 ? intersection / union : 0;
  }

  void dispose() {
    _interpreter?.close();
    _interpreter = null;
    _isModelLoaded = false;
  }
}
