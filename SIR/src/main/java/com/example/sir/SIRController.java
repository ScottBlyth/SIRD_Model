package com.example.sir;


import com.example.sir.server.PyListener;
import com.example.sir.server.PyServer;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleButton;
import javafx.scene.input.KeyCode;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Paint;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.text.Text;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.io.*;
import java.util.*;
import java.util.List;
import java.util.stream.Stream;

public class SIRController {
    @FXML
    private TextFieldClass populationText;
    @FXML
    private LineChart<Number, Number> epiChart;
    @FXML
    private Pane cityGraph;

    @FXML
    private Text selectText;
    @FXML
    private ToggleButton T0;
    @FXML
    private ToggleButton T1;
    @FXML
    private ToggleButton T2;
    @FXML
    private ToggleButton T3;

    @FXML
    private TextField infectivity;
    @FXML
    private TextField recovery;
    @FXML
    private TextField mortality;
    @FXML
    private TextField immunity;

    private final List<String> toggleNames = Arrays.asList("S",  "I", "R", "D");

    private boolean selectedNode = false;
    private Integer vertexSelected = -1;
    private Circle nodeSelected;
    private Graph graph = new Graph();
    private List<Circle> circles = new ArrayList<>();

    private Mode mode = Mode.ADD_NODE;
    private JSONObject data;

    @FXML
    public void initialize() {
        epiChart.setCreateSymbols(false);
        populationText.setGraph(graph);

        populationText.textProperty().addListener((obs, old, new_text) -> {
            if(!new_text.matches("\\d+\\.?\\d*|^$")) {
                populationText.setText(old);
            }
            if(mode == Mode.EDIT_NODE) {
                //vertexSelected
                populationText.readText();
                populationText.ChangePopulation(vertexSelected);
            }
        });
        List<TextField> fields = Arrays.asList(infectivity, recovery, mortality, immunity);
        fields.forEach(x -> x.textProperty().addListener((obs, old, new_text) -> {
            if(!new_text.matches("\\d+\\.?\\d*|^$")) {
                x.setText(old);
            }
        }));

    }

    @FXML
    public void clearPlot() {
        while(!epiChart.getData().isEmpty()) {
            epiChart.getData().removeLast();
        }
    }

    private void updatePopulations() {
        GraphFactory.readPopulations(data, graph);
    }

    private void plotData(int id) {
        List<ToggleButton> toggles = Arrays.asList(T0, T1,T2,T3);
        List<Integer> indices = new ArrayList<>(Stream.of(0, 1, 2, 3).filter(i -> toggles.get(i).isSelected()).toList());
        for(Integer i : indices) {
            XYChart.Series<Number, Number> series = new XYChart.Series<>();
            JSONObject obj = (JSONObject) data.get(String.valueOf(id));
            JSONArray points = (JSONArray) obj.get("points");
            double startTime = 1;
            for(Object array : points) {
                JSONArray arr = (JSONArray) array;
                double time;
                try {
                    time = (double) arr.get(0);
                }catch (Exception e) {
                    time = (double) (long) arr.get(0);
                }
                JSONArray point = (JSONArray) arr.get(1);
                // let us just plot infections for now
                if(startTime >= 1) {
                    double infections = (double) point.get(i);
                    series.getData().add(new XYChart.Data<>(time, infections));
                    startTime = 0;
                }
                startTime += time;
            }
            if(series.getData().isEmpty()) {
                continue;
            }
            series.setName(toggleNames.get(i)+": "+id);
            epiChart.getData().add(series);
        }

    }

    @FXML
    public void setPlot() {
        mode = Mode.PLOT;
    }

    @FXML
    public void saveData() throws IOException {
        JFileChooser chooser = new JFileChooser(".");
        int returnVal = chooser.showOpenDialog(null);
        String path = chooser.getSelectedFile().getPath();

        FileWriter writer = new FileWriter(path);
        writer.write(data.toJSONString());
        writer.close();

    }

    private Circle addCircle(int circleID, double x, double y) {
        Circle circle = new Circle(x, y, 25);
        circle.setId("C"+circleID);
        circle.setOnMouseClicked(mouseEvent1 -> {
            if(mode == Mode.PLOT) {
                plotData(circleID);
            }
            if(selectedNode){
                if(vertexSelected == circleID) {
                    resetSelection();
                }else {
                    if(mode == Mode.LINK) {
                        addLink(nodeSelected, circle);
                        addLink(nodeSelected, circle);

                        graph.addEdge(vertexSelected, circleID, 0.01f);
                        graph.addEdge(circleID, vertexSelected, 0.01f);
                        // deselect everything
                    } else if (mode == Mode.EDIT_EDGES) {
                        int v = vertexSelected;
                        selectText.setText(v+","+circleID);
                        try {
                            populationText.setText(graph.getWeight(vertexSelected, circleID).toString());
                        } catch (Exception e) {
                            throw new RuntimeException(e);
                        }
                    }
                    resetSelection();
                }
                // else selected node
            }else {
                selectedNode = true;
                vertexSelected = circleID;
                nodeSelected = circle;
                circle.setFill(Paint.valueOf("black"));
            }
            if(mode == Mode.EDIT_NODE) {
                populationText.setText(graph.getPopulation(circleID).toString());
                vertexSelected = circleID;
                populationText.setOnKeyPressed(keyEvent -> {
                        populationText.readText();
                        populationText.ChangePopulation(circleID);
                });
            }

        });
        circles.add(circle);
        cityGraph.getChildren().add(circle);
        circle.getStyleClass().add("node");
        return circle;
    }

    @FXML
    public void computeModel() {
        List<Double> params = Stream.of(infectivity.getText(), recovery.getText(), mortality.getText(), immunity.getText()).map(Double::parseDouble).toList();
        PyListener listener = new PyListener(6666, populationText.getText(), graph, params);
        Thread thread = new Thread(() -> {
            listener.run();
            data = listener.getData();
            updatePopulations();
        });
        thread.start();
    }

    @FXML
    public void editParameters() {
        mode = Mode.EDIT_NODE;
    }

    @FXML
    public void clickOnGraph(MouseEvent mouseEvent) {
        if(mode == Mode.ADD_NODE) {
            resetSelection();
            graph.addNode();
            addCircle(graph.numNodes()-1, mouseEvent.getX(), mouseEvent.getY());
        }
    }

    @FXML
    public void toggleCreateNode() {
        mode = Mode.ADD_NODE;
    }

    @FXML
    public void toggleCreateLink() {
        mode = Mode.LINK;
    }

    @FXML
    public void toggleReadEdge() {
        mode = Mode.EDIT_EDGES;
    }

    @FXML
    public void deleteAllNodes() {
        resetSelection();
        for(Circle circle : circles) {
            Node parent = circle.getParent();
            if(parent instanceof Pane) {
                ((Pane) parent).getChildren().remove(circle);
            }
        }
        Node node;
        while((node = cityGraph.getScene().lookup("#link")) != null) {
            cityGraph.getChildren().remove(node);
        }
        graph = new Graph();
        circles = new ArrayList<>();
        populationText.setGraph(graph);
    }

    @FXML
    public void save() throws IOException {
        List<Tuple<Double, Double>> positions = new ArrayList<>();
        for(Circle circle : circles) {
            positions.add(new Tuple<>(circle.getCenterX(), circle.getCenterY()));
        }
        JFileChooser chooser = new JFileChooser(".");
        int returnVal = chooser.showOpenDialog(null);
        if(returnVal == JFileChooser.APPROVE_OPTION) {
            FileWriter writer = new FileWriter(chooser.getSelectedFile().getPath());
            writer.write(graph.toJson(positions).toJSONString());
            writer.close();
        }
    }

    @FXML
    public void load() throws IOException, ParseException {
        JFileChooser chooser = new JFileChooser(".");
        FileNameExtensionFilter filter = new FileNameExtensionFilter("json files","json");
        chooser.setFileFilter(filter);
        int returnVal = chooser.showOpenDialog(null);
        if(returnVal == JFileChooser.APPROVE_OPTION) {
            String filePath = chooser.getSelectedFile().getPath();
            File file = new File(filePath);
            InputStream stream = new FileInputStream(file);
            String jsonText = new String(stream.readAllBytes());
            JSONParser parser = new JSONParser();
            JSONObject jsonObject = (JSONObject) parser.parse(jsonText);

            graph = GraphFactory.loadGraph(jsonObject);
            populationText.setGraph(graph);
            // close stream/file
            stream.close();
            Map<String, Circle> circleMap = new HashMap<>();
            for(String key : (Set<String>) jsonObject.keySet()) {
                JSONObject node = (JSONObject) jsonObject.get(key);
                JSONArray arr = (JSONArray) node.get("position");
                int u = Integer.parseInt(key);
                Circle circle = addCircle(u, (double) arr.get(0), (double) arr.get(1));
                circleMap.put(key, circle);
            }
            // adding the links/edges
            for(String key : (Set<String>) jsonObject.keySet()) {
                JSONObject node = (JSONObject) jsonObject.get(key);
                JSONArray neighbours = (JSONArray) node.get("neighbours");
                for(Object tuple : neighbours) {
                    JSONArray edge = (JSONArray) tuple;
                    Integer v = (int) (long) edge.get(0);
                    Circle first = circleMap.get(key);
                    Circle second = circleMap.get(String.valueOf(v));
                    addLink(first, second);
                }
            }

        }
    }

    private void addLink(Circle firstNode, Circle secondNode) {
        Line line = createLine(firstNode.getCenterX(), firstNode.getCenterY(), secondNode.getCenterX(), secondNode.getCenterY(), secondNode.getRadius());
        cityGraph.getChildren().add(line);
    }

    private void resetSelection() {
        if(!selectedNode) {
            return;
        }
        selectedNode = false;
        vertexSelected=-1;
        nodeSelected.setFill(Paint.valueOf("rgba(0,0,0,0)"));
        nodeSelected = null;
    }

    private Line createLine(double sx, double sy, double ex, double ey, double r) {
        Line line = new Line();
        double diffX = ex-sx;
        double diffY = ey-sy;
        double size = Math.sqrt(diffX*diffX+diffY*diffY);
        diffX /= size;
        diffY /= size;
        sx = sx + r * diffX;
        sy = sy + r * diffY;
        ex = ex - r*diffX;
        ey = ey - r*diffY;
        line.setStartX(sx);
        line.setStartY(sy);
        line.setEndX(ex);
        line.setEndY(ey);
        line.setStrokeWidth(3);
        line.setFill(Paint.valueOf("red"));
        line.setStroke(Paint.valueOf("red"));
        line.setId("link");
        return line;
    }
}
