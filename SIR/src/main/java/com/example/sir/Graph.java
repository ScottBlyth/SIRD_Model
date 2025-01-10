package com.example.sir;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

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
    public String toJson() {
        StringBuilder object = new StringBuilder("{");
        int i = 0;
        for(ArrayList<Tuple<Integer, Float>> neighbours : nodes){
            String key = "\""+i+"\"";
            String comma = ",\n";
            if(i == nodes.size()-1) {
                comma = "\n";
            }
            object.append(key).append(":").append(neighbours).append(comma);
            i++;
        }
        object.append("}");
        return object.toString();
    }
}
