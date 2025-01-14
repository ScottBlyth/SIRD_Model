package com.example.sir;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.*;
import java.util.Scanner;
import java.util.Set;

public class GraphFactory {
    public Graph createGraph(String fileName) throws IOException, ParseException {
        Graph graph = new Graph();
        File file = new File(fileName);
        if(file.exists()) {
            Scanner reader = new Scanner(file);
            StringBuilder text = new StringBuilder();
            while(reader.hasNextLine()) {
                text.append(reader.nextLine());
            }
            JSONParser parser = new JSONParser();
            JSONObject object = (JSONObject) parser.parse(text.toString());
            for(int i = 0; i < object.size(); i++){
                graph.addNode();
            }
            for(String entry : (Set<String>) object.keySet()) {
                Integer u = Integer.valueOf(entry);
                JSONObject iObject = (JSONObject) object.get(entry);
                JSONArray array = (JSONArray) iObject.get("neighbours");
                for(Object obj : array) {
                    JSONArray edge = (JSONArray) obj;
                    // out vertex
                    Integer v = (int) (long) edge.get(0);
                    Float weight = (float) (double) edge.get(1);
                    graph.addEdge(u, v, weight);
                }
            }

        }
        return graph;
    }
}
