import * as echarts from "echarts/core";
import swedenGeoJSON from "../assets/sweden-counties.json";

let registered = false;

export function useSwedenmMap() {
  if (!registered) {
    echarts.registerMap("sweden", swedenGeoJSON as never);
    registered = true;
  }
}
