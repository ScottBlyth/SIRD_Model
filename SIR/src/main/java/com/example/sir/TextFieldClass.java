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
    }

}
