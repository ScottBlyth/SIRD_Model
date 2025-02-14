package com.example.sir.server;

import com.example.sir.Graph;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;

public class PyServer implements Runnable {

    private final int port;
    private ServerSocket socket;
    private Socket s;
    private DataOutputStream out;
    private final Graph graph;
    private boolean toClose = false;
    private List<Double> disease;

    public PyServer(int port, Graph graph, List<Double> disease) {
        this.port = port;
        this.graph = graph;
        this.disease = disease;
    }

    public void close() throws IOException {
        toClose = true;
        s.close();
        socket.close();
    }

    private void sendJsonObject() throws IOException {
        JSONObject obj = graph.toJson();
        JSONArray dObj = new JSONArray();
        dObj.addAll(this.disease);
        obj.put("disease", dObj);
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
