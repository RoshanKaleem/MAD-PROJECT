import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:video_player/video_player.dart';
import 'package:http/http.dart';
import 'package:flappy_search_bar/flappy_search_bar.dart';
import 'dart:ui' as ui;
// import 'package:image_utils_class/image_utils_class.dart';

class Search extends StatelessWidget {
  const Search({Key? key}) : super(key: key);

  Future<List<Widget>> search(String search) async {
    var url = Uri.parse('http://10.0.2.2:5000/images');
    var response = await post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'title': search,
      }),
    );

    var img_url = jsonDecode(response.body);
    List<Widget> res = List.generate(img_url.length, (int index) {
      return Image.network(img_url[index], fit: BoxFit.fitWidth);
    });

    // print(json.decode(response.body)['ImageBytes'].length);
    if (res.length == 0) {}

    return res;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: SearchBar<Widget>(
            crossAxisCount: 2,
            onSearch: search,
            onItemFound: (Widget post, int index) {
              print('hello');
              print(post);
              print(index);
              return Padding(
                padding: const EdgeInsets.all(5.0),
                child: post,
              );
            },
          ),
        ),
      ),
    );
  }
}
