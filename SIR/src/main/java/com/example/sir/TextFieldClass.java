package com.example.sir;


import java.util.Arrays;

public class TextFieldClass extends javafx.scene.control.TextField  {
    private Graph graph;
    private String text;

    public TextFieldClass() {
        this.text = getText();
    }
    public void setGraph(Graph graph) {
        this.graph = graph;
    }
    private String getParsedText() {
        return text;
    }

    public void readText() {
        if(getText().matches("\\d+\\.?\\d*")) {
            System.out.println("matched!");
            text = getText();
        }else {
            setText(text);
        }
    }


    public void ChangePopulation(Integer circleID) {
        graph.setPopulation(circleID, Arrays.asList(Integer.parseInt(getParsedText()), 0, 0, 0));
        System.out.println(graph.getPopulation(circleID));
    }
    public void changeWeight(Integer u, Integer v) {
        try {
            graph.changeWeight(u, v, Float.parseFloat(getParsedText()));
        }catch (Exception e){

        }

        try {
            System.out.println(graph.getWeight(u,v));
        } catch (Exception e) {
            System.out.println(graph.toJson().toJSONString());
        }

    }
}
