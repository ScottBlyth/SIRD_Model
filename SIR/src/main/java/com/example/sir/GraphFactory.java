package com.example.sir;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.*;

public class GraphFactory {

    public static void readPopulations(JSONObject data, Graph graph) {
        for(Object obj : data.keySet()) {
            String key = (String) obj;
            Integer u = Integer.parseInt(key);
            JSONArray population =  (JSONArray) ((JSONObject) data.get(key)).get("population");
            List<Integer> integers = new ArrayList<>(population.size());
            for(Object number : population) {
                Double num = (double) number;
                integers.add((int) num.longValue());
            }
            graph.setPopulation(u, integers);
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
