package contest;

import org.jgrapht.Graph;
import org.jgrapht.GraphPath;
import org.jgrapht.Graphs;
import org.jgrapht.alg.interfaces.ShortestPathAlgorithm;
import org.jgrapht.alg.shortestpath.BFSShortestPath;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.generate.GridGraphGenerator;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.graph.SimpleWeightedGraph;

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {

        //Step 1: Fetch data from file
        String inputFilePath = "Level1_contest.in"; // set the name of the input file
        String outputFilePath = "Level1_out_contest.txt"; // set the name of the output file

        int nScenarios = 0;

        try (BufferedReader reader = new BufferedReader(new FileReader(inputFilePath))) {
            PrintWriter writer = new PrintWriter(new FileWriter(outputFilePath));

            String line;

            //Read number of scenarios
            if((line = reader.readLine()) != null) {
                nScenarios = Integer.parseInt(line);
            }
            writer.println(nScenarios);

            for(int i = 0; i < nScenarios; ++i) {
                System.out.println("Starting scenario " + i);
                int gridBoundsX_columns = 0;
                int gridBoundsY_rows = 0;
                int maximumExtraWalls = 0;

                Tile treasure = null;
                Tile entrance = null;

                if((line = reader.readLine()) != null) {
                    String[] substrings;
                    substrings = line.split(" ");
                    gridBoundsX_columns = Integer.parseInt(substrings[0]);
                    gridBoundsY_rows = Integer.parseInt(substrings[1]);
                    maximumExtraWalls = Integer.parseInt(substrings[2]);

                    //Read grid and model it as a graph
                    Graph<Tile, DefaultEdge> dungeonGraph = null;
                    if(gridBoundsY_rows == 1) {
                        //Horizontal path graph
                        dungeonGraph = new SimpleGraph<>(DefaultEdge.class);

                        //Add vertices
                        Tile[] vertices = new Tile[gridBoundsX_columns];
                        if((line = reader.readLine()) != null) {
                            for(int k = 0; k < gridBoundsX_columns; ++k) {
                                vertices[k] = new Tile(line.charAt(k), k, 0);
                                dungeonGraph.addVertex(vertices[k]);
                            }
                        }

                        // Add edges
                        for (int j = 0; j < gridBoundsX_columns - 1; ++j) {
                            dungeonGraph.addEdge(vertices[j], vertices[j + 1]);
                        }
                        writer.println("0");
                        continue;
                    } else if(gridBoundsX_columns == 1) {
                        //Vertical path graph
                        dungeonGraph = new SimpleGraph<>(DefaultEdge.class);

                        //Add vertices
                        Tile[] vertices = new Tile[gridBoundsY_rows];
                        for(int k = 0; k < gridBoundsY_rows; ++k) {
                            if((line = reader.readLine()) != null) {
                                if (line.length() == 1) {
                                    vertices[k] = new Tile(line.charAt(0), 0, k);
                                    dungeonGraph.addVertex(vertices[k]);
                                } else {
                                    System.out.println("Error! vertical path graph has more than one character per line");
                                }
                            }
                        }

                        // Add edges
                        for (int j = 0; j < gridBoundsY_rows - 1; ++j) {
                            dungeonGraph.addEdge(vertices[j], vertices[j + 1]);
                        }
                        writer.println("0");
                        continue;
                    } else {
                        //Grid graph
                        dungeonGraph = new SimpleGraph<>(DefaultEdge.class);

                        //Add vertices
                        Tile[][] vertices = new Tile[gridBoundsX_columns][gridBoundsY_rows];
                        for(int j = 0; j < gridBoundsY_rows; ++j) {
                            if((line = reader.readLine()) != null) {
                                for(int k = 0; k < gridBoundsX_columns; ++k) {
                                    vertices[k][j] = new Tile(line.charAt(k), k, j);
                                    dungeonGraph.addVertex(vertices[k][j]);
                                    if(vertices[k][j].getCharacter() == 'T') {
                                        treasure = vertices[k][j];
                                    }
                                    if(vertices[k][j].getCharacter() == 'E') {
                                        entrance = vertices[k][j];
                                    }
                                }
                            }
                        }

                        // Add edges between adjacent vertices
                        for (int j = 0; j < gridBoundsY_rows; ++j) {
                            for (int k = 0; k < gridBoundsX_columns; ++k) {
                                Tile vertex = vertices[k][j];
                                if (j > 0) {  // Check if there is a vertex above
                                    Tile adjacentVertex = vertices[k][j - 1];
                                    if(vertex.getCharacter() != 'W' && adjacentVertex.getCharacter() != 'W') {
                                        dungeonGraph.addEdge(vertex, adjacentVertex);
                                    }
                                }
                                if (j < gridBoundsY_rows - 1) {  // Check if there is a vertex below
                                    Tile adjacentVertex = vertices[k][j + 1];
                                    if(vertex.getCharacter() != 'W' && adjacentVertex.getCharacter() != 'W') {
                                        dungeonGraph.addEdge(vertex, adjacentVertex);
                                    }
                                }
                                if (k > 0) {  // Check if there is a vertex to the left
                                    Tile adjacentVertex = vertices[k - 1][j];
                                    if(vertex.getCharacter() != 'W' && adjacentVertex.getCharacter() != 'W') {
                                        dungeonGraph.addEdge(vertex, adjacentVertex);
                                    }
                                }
                                if (k < gridBoundsX_columns - 1) {  // Check if there is a vertex to the right
                                    Tile adjacentVertex = vertices[k + 1][j];
                                    if(vertex.getCharacter() != 'W' && adjacentVertex.getCharacter() != 'W') {
                                        dungeonGraph.addEdge(vertex, adjacentVertex);
                                    }
                                }
                            }
                        }
                    }
                    //System.out.println(dungeonGraph);
                    //Step 2: Find solution

                    BFSShortestPath<Tile, DefaultEdge> bfs = new BFSShortestPath<>(dungeonGraph);
                    GraphPath<Tile, DefaultEdge> initialShortestPath = bfs.getPath(entrance, treasure);
                    int initialShortestPathLength = initialShortestPath.getLength();
                    int extraAddedWallsCount = 0;
                    ArrayList<Tile> addedWalls = new ArrayList<>();


                    //Get all neighbors of initial shotest path
                    Graph<Tile, DefaultEdge> graph = initialShortestPath.getGraph();
                    List<Tile> pathVertices = initialShortestPath.getVertexList();
                    Set<Tile> neighboringVertices = new HashSet<>();
                    for(int j = 0; j < pathVertices.size(); ++j) {
                        Tile vertex = pathVertices.get(j);
                        Set<DefaultEdge> outgoingEdges = graph.outgoingEdgesOf(vertex);
                        for(DefaultEdge e : outgoingEdges) {
                            neighboringVertices.add(graph.getEdgeTarget(e));
                        }
                    }

                    //Iterate over all vertices from path and try to add a wall
                    Iterator<Tile> vertexIterator = neighboringVertices.iterator();
                    for(int j = 0; j < neighboringVertices.size(); ++j) {
                        Tile tempVertex = vertexIterator.next();
                        if(tempVertex.getCharacter() != 'T' && tempVertex.getCharacter() != 'E' && tempVertex.getCharacter() != 'W') {
                            //Add a wall and isolate vertex
                            tempVertex.setCharacter('W');
                            Set<DefaultEdge> removedEdges = new HashSet<>(dungeonGraph.edgesOf(tempVertex));
                            dungeonGraph.removeAllEdges(removedEdges);

                            GraphPath<Tile, DefaultEdge> shortestPath = bfs.getPath(entrance, treasure);
                            if(shortestPath != null && shortestPath.getLength() > initialShortestPathLength && extraAddedWallsCount <= maximumExtraWalls) {
                                addedWalls.add(tempVertex);
                                ++extraAddedWallsCount;
                                j = 0; //Start over with newly improved dungeon
                                vertexIterator = neighboringVertices.iterator(); //reset iterator as well
                            } else {
                                //Undo addition of wall
                                tempVertex.setCharacter('.');
                                for (DefaultEdge edge : removedEdges) {
                                    dungeonGraph.addEdge(dungeonGraph.getEdgeSource(edge), dungeonGraph.getEdgeTarget(edge));
                                }
                            }
                        }
                    }

                    //Write solution in output file
                    writer.println(extraAddedWallsCount);
                    for(int j = 0; j < extraAddedWallsCount; ++j) {
                        writer.print(addedWalls.get(j).getX_col() + " " + addedWalls.get(j).getY_row());
                        if(j != extraAddedWallsCount - 1) {
                            writer.print(" ");
                        }
                    }
                    writer.print("\n");

                    //System.out.println("Shortest path: " + initialShortestPath.getVertexList());
                }
            }

            reader.close(); // close the Reader object to flush the buffer and release the resources
            writer.close(); // close the PrintWriter object to flush the buffer and release the resources
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }
}
