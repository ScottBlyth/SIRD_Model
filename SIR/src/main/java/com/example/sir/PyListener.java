package com.example.sir;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class PyListener {

    private ServerSocket socket;
    private Socket s;
    private DataInputStream in;
    private JSONObject obj;

    public PyListener(int port) throws IOException, ParseException {
        socket = new ServerSocket(port);
        // wait for client
        s = socket.accept();
        in = new DataInputStream(new BufferedInputStream(s.getInputStream()));
        JSONParser parser = new JSONParser();
        obj = (JSONObject) parser.parse(String.valueOf(in));
    }

    public JSONObject getObj(){return obj;}

}
