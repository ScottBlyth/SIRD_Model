package com.example.sir.server;

import com.example.sir.Graph;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class PyServer implements Runnable {

    private int port;
    private ServerSocket socket;
    private Socket s;
    private DataOutputStream out;
    private Graph graph;
    private boolean toClose = false;

    public PyServer(int port, Graph graph) throws IOException, ParseException {
        this.port = port;
        this.graph = graph;
    }

    public void close() throws IOException {
        toClose = true;
        s.close();
        socket.close();
    }

    private void sendJsonObject() throws IOException {
        JSONObject obj = graph.toJson();
        out.writeUTF(obj.toJSONString());
        out.flush();
    }

    @Override
    public void run() {
        try {
            socket = new ServerSocket(port);
            // wait for client
            while(!toClose) {
                s = socket.accept();
                System.out.println("connected...");
                out = new DataOutputStream(new BufferedOutputStream(s.getOutputStream()));
                this.sendJsonObject();
                System.out.println("Sent graph!");
                out.close();
                s.close();
                System.out.println("Closed Connection...");
            }
            socket.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}
