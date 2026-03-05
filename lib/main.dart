
import 'package:flutter/material.dart';

void main() {
  runApp(SimpleUI());
}

class SimpleUI extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(useMaterial3: true),
      home: Scaffold(
        appBar: AppBar(
          title: Text("Mi Interfaz Sencilla"),
          centerTitle: true,
        ),
        body: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [

              // -------- TARJETA 1 --------
              Card(
                color: Colors.grey[900],
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
                child: ListTile(
                  leading: Icon(Icons.thermostat, size: 40, color: Colors.orange),
                  title: Text("Temperatura"),
                  subtitle: Text("24.5 °C"),
                ),
              ),

              SizedBox(height: 20),

              // -------- TARJETA 2 --------
              Card(
                color: Colors.grey[900],
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
                child: ListTile(
                  leading: Icon(Icons.water_drop, size: 40, color: Colors.blue),
                  title: Text("Humedad"),
                  subtitle: Text("62 %"),
                ),
              ),

              SizedBox(height: 40),

              // -------- BOTÓN --------
              ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  minimumSize: Size(double.infinity, 50),
                  backgroundColor: Colors.green,
                ),
                child: Text("Botón de prueba"),
              ),

            ],
          ),
        ),
      ),
    );
  }
}
