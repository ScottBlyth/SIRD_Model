package com.example.sir;

import org.json.simple.JSONArray;

public class Tuple<T,V> {
    private T v1;
    private V v2;
    public Tuple(T v1, V v2) {
        this.v1 = v1;
        this.v2 = v2;
    }
    public T v1() {
        return v1;
    }

    public void setV1(T v1) {
        this.v1 = v1;
    }

    public V v2() {
        return v2;
    }

    public void setV2(V v2) {
        this.v2 = v2;
    }

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
