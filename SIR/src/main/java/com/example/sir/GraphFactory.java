package com.example.sir;

import javafx.scene.shape.Circle;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

public class GraphFactory {
    public void changePopulations(JSONObject data)  {
        for (Object key : data.keySet()) {

        }
    }

    public static Graph loadGraph(JSONObject jsonObject) {
        Graph graph = new Graph();
        Integer i = 0;
        for(String key : (Set<String>) jsonObject.keySet()) {
            JSONObject node = (JSONObject) jsonObject.get(key);
            JSONArray population = (JSONArray) node.get("population");
            List<Integer> integers = new ArrayList<>(population.size());
            for(Object obj : population) {
                long num = (long) obj;
                integers.add((int) num);
            }
            graph.addNode();
            graph.setPopulation(i, integers);
            i++;
        }
        // adding the links/edges
        for(String key : (Set<String>) jsonObject.keySet()) {
            JSONObject node = (JSONObject) jsonObject.get(key);
            JSONArray neighbours = (JSONArray) node.get("neighbours");
            for(Object tuple : neighbours) {
                JSONArray edge = (JSONArray) tuple;
                Integer v = (int) (long) edge.get(0);
                double weight = (double) edge.get(1);
                graph.addEdge(Integer.parseInt(key), v, (float) weight);
            }
        }
        return graph;
    }
}
