import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Logavu',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(useMaterial3: true),
      home: const MyHomePage(title: 'Logavu'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final List<LogMessage> _messages = [];
  bool isRecording = false;
  MethodChannel platform = const MethodChannel('logavu');

  @override
  void initState() {
    super.initState();

    // Register a listener on the channel.
    platform.setMethodCallHandler((MethodCall call) {
      switch (call.method) {
        case 'on_message':
          setState(() {
            var text = call.arguments;
            _messages.add(LogMessage(text: text));
          });
          break;
      }
      return Future(() => null);
    });
  }

  final ScrollController _scrollController = ScrollController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        //backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Scrollbar(
        thumbVisibility: true,
        controller: _scrollController,
        child: ListView.builder(
          controller: _scrollController,
          itemCount: _messages.length,
          itemBuilder: (context, index) {
            return Container(
              color: index % 2 == 0 ? Colors.grey[900] : Colors.grey[850],
              padding: const EdgeInsets.all(8.0),
              child: Text(_messages[index].text),
            );
          },
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              IconButton(
                icon: Icon(isRecording ? Icons.pause : Icons.record_voice_over),
                onPressed: () {
                  setState(() {
                    isRecording = !isRecording;
                  });
                },
              ),
              IconButton(
                icon: const Icon(Icons.add_comment),
                onPressed: () {
                  setState(() {
                    _messages.add(LogMessage(text: 'Test Log Message'));
                  });
                },
              ),
              IconButton(
                icon: const Icon(Icons.delete),
                onPressed: () {
                  setState(() {
                    _messages.clear();
                  });
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class LogMessage {
  String text;
  LogMessage({required this.text});
}
