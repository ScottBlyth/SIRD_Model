package com.example.sir;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;

public record Tuple<T, V>(T v1, V v2) {

    @Override
    public String toString() {
        return "["+v1+","+v2+"]";
    }

    public JSONArray toJSon() {
        JSONArray arr = new JSONArray();
        arr.add(v1);
        arr.add(v2);
        return arr;
    }

}
