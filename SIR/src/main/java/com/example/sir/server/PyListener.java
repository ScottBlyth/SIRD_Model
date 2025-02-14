package com.example.sir.server;

import com.example.sir.Graph;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.*;
import java.net.Socket;
import java.util.List;

public class PyListener implements Runnable {

    private Socket socket;
    private final int port;
    private final String time;
    private JSONObject data;
    private final Graph graph;
    private List<Double> disease;

    public PyListener(int port, String time, Graph graph, List<Double> disease) {
        this.port = port;
        this.time = time;
        this.graph = graph;
        this.disease = disease;
    }

    public JSONObject getData() {
        return data;
    }

    @Override
    public void run() {
        try {
            // requests data
            socket = new Socket("localhost", port);
            DataOutputStream out = new DataOutputStream(socket.getOutputStream());

            JSONObject obj = graph.toJson();
            JSONArray dObj = new JSONArray();
            dObj.addAll(this.disease);
            obj.put("disease", dObj);

            out.writeUTF("num"+ time +obj.toJSONString());
            out.flush();

            System.out.println("Sent Request!");

            BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            StringBuilder builder = new StringBuilder();
            String dataString = "";
            while((dataString = reader.readLine()) != null) {
                builder.append(dataString);
            }
            dataString = builder.toString();
            System.out.println("reading...");

            reader.close();
            out.close();
            socket.close();

            JSONParser parser = new JSONParser();
            data = (JSONObject) parser.parse(dataString);

            System.out.println("Got Data!!");
        } catch (IOException | ParseException e) {
            throw new RuntimeException(e);
        }
    }
}
