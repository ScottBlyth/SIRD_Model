package com.example.sir;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Graph {

    private final ArrayList<ArrayList<Tuple<Integer, Float>>> nodes = new ArrayList<>();

    public void addNode() {
        nodes.add(new ArrayList<>());
    }
    public boolean hasEdge(Integer u, Integer v) {
        return nodes.get(u).stream().anyMatch(t -> Objects.equals(t.v1(), v));
    }
    public void addEdge(Integer u, Integer v, Float weight) {
        if(this.hasEdge(u,v)) {
            return;
        }
        nodes.get(u).add(new Tuple<>(v, weight));
    }
    public Integer numNodes(){
        return nodes.size();
    }

    public JSONObject toJson(List<Tuple<Double, Double>> positions) {
        int i = 0;
        JSONObject jsonObject = new JSONObject();
        for(ArrayList<Tuple<Integer, Float>> neighbours : nodes) {
            // vertex i
            JSONObject iObject = new JSONObject();
            JSONArray neighbourArray = new JSONArray();
            for(Tuple<Integer, Float> edge : neighbours) {
                JSONArray arr = edge.toJSon();
                neighbourArray.add(arr);
            }
            iObject.put("neighbours", neighbourArray);
            iObject.put("position", positions.get(i).toJSon());
            jsonObject.put(String.valueOf(i), iObject);
            // increment i
            i++;
        }
        return jsonObject;
    }
}
