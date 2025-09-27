import 'package:flutter/material.dart';
import 'package:universal_html/html.dart' as html;
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:ui_web' as ui;

class CameraScreen extends StatelessWidget {
  final String streamUrl;

  const CameraScreen({Key? key, required this.streamUrl}) : super(key: key);

  Future<String> fetchDataFromBackend() async {
    // Simulate a network call
    await Future.delayed(Duration(seconds: 2));
    return "Data from backend"; // Replace this with actual data fetching logic
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Disease Detection Cam"),backgroundColor:Colors.green.shade50,foregroundColor:Colors.black),
      body: Column(
        children: [
          SizedBox(height:20),
          Center(
            child: SizedBox(

              height:450,
              width:450,
              child: Container(
                decoration:BoxDecoration(
                  borderRadius:BorderRadius.circular(16),

                ),
                child:ClipRRect(
                  borderRadius:BorderRadiusGeometry.circular(20),
                  child: IPhoneCameraStream(
                    streamUrl: streamUrl, // Use the passed stream URL
                  ),
                )

              ),
            ),

          ),
          DraggableScrollableSheet(
              initialChildSize:0.45,
              minChildSize:0.2,
              maxChildSize:0.85,builder: (context, scrollController){
                return Container(
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(20),
                      topRight: Radius.circular(20),
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black26,
                        blurRadius: 10,
                        offset: Offset(0, -2),
                      )
                    ],
                  ),
                  padding:const EdgeInsets.all(20),
                  child: Column(
                    children:[
                        Card(

                        )
                    ]
                  )
                );
          }),
          FutureBuilder<String>(
            future: fetchDataFromBackend(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return CircularProgressIndicator();
              } else if (snapshot.hasError) {
                return Text("Error: ${snapshot.error}");
              } else {
                return Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text("Fetched Data: ${snapshot.data}"),
                );
              }
            },
          ),
        ],
      ),
    );
  }
}

class IPhoneCameraStream extends StatefulWidget {
  final String streamUrl;
  const IPhoneCameraStream({super.key, required this.streamUrl});

  @override
  State<IPhoneCameraStream> createState() => _IPhoneCameraStreamState();
}

class _IPhoneCameraStreamState extends State<IPhoneCameraStream> {
  html.MediaStream? _stream;
  bool _isStreaming = false;


  @override
  void initState() {
    super.initState();
    _startCamera();
  }

  Future<void> _startCamera() async {
    try {
      final stream = await html.window.navigator.mediaDevices!.getUserMedia({
        'video': {
          'width': 640,
          'height': 480,
          'facingMode': 'environment',
        },
        'audio': false,
      });

      setState(() {
        _stream = stream;
        _isStreaming = true;
      });

      ui.platformViewRegistry.registerViewFactory(
        'web-camera',
            (int viewId) {
          final video = html.VideoElement()
            ..srcObject = stream
            ..autoplay = true
            ..muted = true
            ..style.width = '100%'
            ..style.height = '100%'
            ..style.objectFit = 'cover';
          return video;
        },
      );
    } catch (e) {
      print("Error starting camera: $e");
      ui.platformViewRegistry.registerViewFactory(
        'web-camera',
            (int viewId) {
          final element = html.ImageElement()
            ..src = widget.streamUrl
            ..style.width = '100%'
            ..style.height = '100%'
            ..style.objectFit = 'cover';
          return element;
        },
      );
    }
  }

  Future<void> _capturePhoto() async {
    if (_stream == null) return;
    try {
      final video = html.VideoElement()
        ..srcObject = _stream
        ..width = 640
        ..height = 480;

      await video.play();
      await Future.delayed(const Duration(milliseconds: 100));

      final canvas = html.CanvasElement(width: 640, height: 480);
      final ctx = canvas.context2D;

      // ✅ Correct usage
      ctx.drawImage(video, 0, 0);

      final dataUrl = canvas.toDataUrl('image/jpeg', 0.8);
      final base64Image = dataUrl.split(',')[1];

      final response = await http.post(
        Uri.parse("http://172.25.25.140:8000/video_feed"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"image": base64Image}),
      );

      if (response.statusCode == 200) {
        print("Photo captured and sent successfully!");
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text("Photo captured and sent successfully!")),
          );
        }
      } else {
        print("Error sending photo: ${response.statusCode}");
      }
    } catch (e) {
      print("Error capturing photo: $e");
    }
  }

  @override
  void dispose() {
    _stream?.getTracks().forEach((track) => track.stop());
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Register a <img> element that streams MJPEG from backend
    // ignore: undefined_prefixed_name
    ui.platformViewRegistry.registerViewFactory(
      'iphone-camera',
          (int viewId) {
        final element = html.ImageElement()
          ..src = 'http://172.25.25.140:8000/video_feed'
          ..style.width = '100%'     // responsive
          ..style.height = '100%'
          ..style.objectFit = 'cover'
          ..style.border = 'none';
        return element;
      },
    );

    return const Scaffold(
      body: Center(
        child: HtmlElementView(viewType: 'iphone-camera'),
      ),
    );
  }
}
