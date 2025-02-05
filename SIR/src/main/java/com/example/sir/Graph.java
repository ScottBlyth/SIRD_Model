package com.example.sir;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

public class Graph {

    private final ArrayList<ArrayList<Tuple<Integer, Float>>> nodes = new ArrayList<>();
    private final ArrayList<Integer> populations = new ArrayList<>();
    public void addNode() {
        nodes.add(new ArrayList<>());
        populations.add(1000); // just for now
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

    public Float getWeight(Integer u, Integer v) throws Exception {
        if(!this.hasEdge(u,v)) {
            throw new Exception("edge doesn't exist");
        }
        return nodes.get(u).stream().filter(t -> Objects.equals(t.v1(), v)).findFirst().get().v2();
    }

    public Integer getPopulation(Integer u) {
        return populations.get(u);
    }

    public void setPopulation(Integer u, Integer population) {
        populations.set(u, population);
    }

    public void changeWeight(Integer u, Integer v, Float weight) {
        // find edge
        Optional<Tuple<Integer, Float>> edge = nodes.get(u).stream().filter(t -> Objects.equals(t.v1(), v)).findFirst();
        // change edge weight
        edge.ifPresent(tup -> tup.setV2(weight));
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
            if(i < positions.size()) {
                iObject.put("position", positions.get(i).toJSon());
            }
            iObject.put("population", populations.get(i));
            jsonObject.put(String.valueOf(i), iObject);
            // increment i
            i++;
        }
        return jsonObject;
    }
    public JSONObject toJson() {
        return toJson(new ArrayList<>());
    }

}
