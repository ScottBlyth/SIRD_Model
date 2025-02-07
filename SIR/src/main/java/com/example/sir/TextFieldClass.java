package com.example.sir;

public class TextFieldClass extends javafx.scene.control.TextField  {
    private Graph graph;

    public TextFieldClass() {
    }
    public void setGraph(Graph graph) {
        this.graph = graph;
    }
    public void ChangePopulation(Integer circleID) {
        graph.setPopulation(circleID, Integer.parseInt(getText()));
        System.out.println(graph.getPopulation(circleID));
    }
    public void changeWeight(Integer u, Integer v) {
        try {
            graph.changeWeight(u, v, Float.parseFloat(getText()));
        }catch (Exception e){

        }
        /*
        try {
            System.out.println(graph.getWeight(u,v));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        */
    }
}
