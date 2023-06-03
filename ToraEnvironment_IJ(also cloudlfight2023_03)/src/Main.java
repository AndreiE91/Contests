import org.jgrapht.Graph;
import org.jgrapht.GraphPath;
import org.jgrapht.alg.interfaces.ShortestPathAlgorithm;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.SimpleWeightedGraph;

import java.io.*;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Set;

public class Main {
    public static void main(String[] args) {
        //Set time limit
        final Integer timeLimit = 1000;

        //Step 1: Fetch data from file
        String filePath = "Level1.in"; //set the name of the input file
        int nScenarios = 0;
        ArrayList<Scenario> scenarios = new ArrayList<Scenario>();

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;

            //Read number of scenarios
            if((line = reader.readLine()) != null) {
                nScenarios = Integer.parseInt(line);
            }

            //For each scenario, read all of its relevant information from the input file
            for(int i = 0; i < nScenarios; ++i) {
                int nCities, mRoads, initialGoldAmount;
                if((line = reader.readLine()) != null) {
                    //Create a new array of 3 strings
                    String[] splits = new String[3];
                    splits = line.split(" ");

                    //Create and add new scenario
                    nCities = Integer.parseInt(splits[0]);
                    mRoads = Integer.parseInt(splits[1]);
                    initialGoldAmount = Integer.parseInt(splits[2]); //It is known there are only 3 parameters on this line

                    Scenario newScenario = new Scenario(nCities, mRoads, initialGoldAmount);
                    scenarios.add(newScenario);

                    //Read road information
                    ArrayList<Road> roads = new ArrayList<Road>();
                    for(int j = 0; j < mRoads; ++j) {
                        if((line = reader.readLine()) != null) {
                            int cityA, cityB, distance;
                            String[] roadSplits = new String[3]; //It is known there are only 3 parameters on this line
                            roadSplits = line.split(" ");
                            cityA = Integer.parseInt(roadSplits[0]);
                            cityB = Integer.parseInt(roadSplits[1]);
                            distance = Integer.parseInt(roadSplits[2]);

                            roads.add(new Road(cityA, cityB, distance));
                        }
                    }
                    //After reading all road information, store it into the scenario's road information
                    scenarios.get(i).setRoads(roads);

                    //Now read buying price for city 0
                    if((line = reader.readLine()) != null) {
                        int buyPriceProductCity0 = Integer.parseInt(line);
                        scenarios.get(i).setPriceBuyProductInCity0(buyPriceProductCity0);
                    }

                    //Finally, read all sell prices and store them in the appropriate data structure
                    if((line = reader.readLine()) != null) {
                        String[] sellPricesString = new String[nCities - 1];//Ignore city 0 where merchant starts from
                        sellPricesString = line.split(" ");

                        //j needs to start from 1, because it will be used to associate each city's id with the selling price in a map structure
                        for(int j = 1; j <= sellPricesString.length; ++j) {
                            newScenario.getSellPrices().put(j, Integer.parseInt(sellPricesString[j - 1]));
                        }
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        } catch (InvalidInputDataException e) {
            System.out.println("Error: The suppplied data is either invalid, or the implemented read method has a bug");
            throw new RuntimeException(e);
        }

        //Step 2: Perform computations on the fetched data in order to obtain a solution
        //In order to find the optimal solution, the cities and their connecting roads will be represented as a weighted graph
        //where each edge has a weight corresponding to the distance of its corresponding road


        String fileName = "Level1_out.txt"; // set the name of the output file
        try {
            PrintWriter writer = new PrintWriter(new FileWriter(fileName));
            // create a PrintWriter object with a FileWriter object that writes to the output file
            writer.println(nScenarios); // write the number of scenarios on the first line

            //For each scenario, a solution will be computed and then added into the output file.
            for(int i = 0; i < nScenarios; ++i) {
                //Instantiate a new graph for modeling the scenario
                Graph<City, DefaultWeightedEdge> cityRoadGraph = new SimpleWeightedGraph<>(DefaultWeightedEdge.class);
                ArrayList<City> citiesForCurrentScenario = new ArrayList<City>();
                //Manually add first city with id 0
                citiesForCurrentScenario.add(new City(0, -1 * scenarios.get(i).getPriceBuyProductInCity0()));
                cityRoadGraph.addVertex(citiesForCurrentScenario.get(0));

                //Add all cities as vertices into the graph
                for(int j = 1; j <= scenarios.get(i).getnCities() - 1; ++j) {
                    citiesForCurrentScenario.add(new City(j, scenarios.get(i).getSellPrices().get(j)));
                    cityRoadGraph.addVertex(citiesForCurrentScenario.get(j));
                }
                //Add all roads as weighted edges into the graph
                for(int j = 0; j < scenarios.get(i).getmRoads(); ++j) {
                    int tempCityA = scenarios.get(i).getRoads().get(j).getCityA();
                    int tempCityB = scenarios.get(i).getRoads().get(j).getCityB();
                    if(tempCityA == tempCityB) {
                        //Invalid road
                        continue;
                    }

                    DefaultWeightedEdge edge = cityRoadGraph.addEdge(citiesForCurrentScenario.get(tempCityA), citiesForCurrentScenario.get(tempCityB));

                    cityRoadGraph.setEdgeWeight(edge, scenarios.get(i).getRoads().get(j).getDistance());
                }
                //Here are the steps for obtaining the solution:

                //1.Perform Dijkstra's algorithm(since no negative weight edges can exist)
                //2.Obtain output as a set of reachable set of vertices, along with the sum of all weights from the path to reach them
                //3.Divide sell price by buy price in vertex 0 to obtain profit, then divide said profit by previously computed sum
                //4.Obtain profit per unit of time for all reachable vertices
                //5.Simply repeat circuit of buying from vertex 0 and selling to best scoring vertex until time runs out

                //1.Dijkstra's algorithm
                City sourceVertex = citiesForCurrentScenario.get(0);

                DijkstraShortestPath<City, DefaultWeightedEdge> dijkstra = new DijkstraShortestPath<>(cityRoadGraph);
                ShortestPathAlgorithm.SingleSourcePaths<City, DefaultWeightedEdge> paths = dijkstra.getPaths(sourceVertex);

                //Divide sell price by distance to obtain profit per unit of time
                City mostProfitableSellPlace = citiesForCurrentScenario.get(0); //If this ramains unchanged, then all other cities offer lower sell prices than we can buy so no profits can be made
                for (City vertex : cityRoadGraph.vertexSet()) {
                    if (paths.getPath(vertex) != null) {
                        double distance = paths.getWeight(vertex);
                        vertex.setProfitPerUnitOfTime((vertex.getSellPrice() - scenarios.get(i).getPriceBuyProductInCity0()) / distance);

                        //System.out.println("Vertex " + vertex.getId() + " is reachable from the source vertex with distance " + distance);
                        //System.out.println("Profit potential: " + vertex.getProfitPerUnitOfTime());

                        if(vertex.getProfitPerUnitOfTime() > mostProfitableSellPlace.getProfitPerUnitOfTime()) {
                            mostProfitableSellPlace = vertex;
                        }
                    }
                }
                //System.out.println("Most profitable sell place is city " + mostProfitableSellPlace.getId());

                //Try to maximize little time that's left with other less efficient but closer cities
                //In this case, we'll need to get all reachable vertices and sort them by highest profit/time score
                //and remove one by one the best ones until we find one that fits whatever time there is left
                ArrayList<City> descendingBestCitiesToSell = new ArrayList<City>();
                for (City vertex : cityRoadGraph.vertexSet()) {
                    descendingBestCitiesToSell.add(vertex);
                }

                //Define new comparator to sort cities by efficiency
                Comparator<City> byEfficiency = new Comparator<City>() {
                    @Override
                    public int compare(City o1, City o2) { //Reverse order of arguments for reverse sorting
                        return Double.compare(o2.getProfitPerUnitOfTime(), o1.getProfitPerUnitOfTime());
                    }
                };
                descendingBestCitiesToSell.sort(byEfficiency);
                descendingBestCitiesToSell.remove(mostProfitableSellPlace);
                mostProfitableSellPlace = descendingBestCitiesToSell.get(0);

                //Repeat process of buying from city 0 and selling to found most profitable sell place until time runs out
                int currentTime = timeLimit;
                int actionsCount = 0;
                int currentGold = scenarios.get(i).getInitialGoldAmount();
                int buyPriceCity0 = scenarios.get(i).getPriceBuyProductInCity0();
                ArrayList<String> actionLines = new ArrayList<String>();
                boolean cont = false;
                int amountToBuy = currentGold / buyPriceCity0;

                //Try to see if we have enough to buy at least one unit
                if(amountToBuy == 0) {
                    //No profit to be made, do nothing and move on to next scenario
                    writer.println("0");
                    continue;
                }
                //Try to see if buying is worth it
                if(descendingBestCitiesToSell.get(0).getProfitPerUnitOfTime() <= 0) {
                    //No profit to be made, do nothing and move on to next scenario
                    writer.println("0");
                    continue;
                }

                boolean moveToNextBestCity = false;
                while(!descendingBestCitiesToSell.isEmpty() && currentTime > 0) {
                    double timeTakenToTravelAtSellDestination = paths.getWeight(mostProfitableSellPlace);
                    if(moveToNextBestCity) {
                        moveToNextBestCity = false;
                        descendingBestCitiesToSell.remove(mostProfitableSellPlace);
                        if(!descendingBestCitiesToSell.isEmpty()) {
                            mostProfitableSellPlace = descendingBestCitiesToSell.get(0);
                        }
                    }

                    currentGold %= buyPriceCity0;
                    //Only buy if there is enough time to sell and realize profit
                    if(currentTime - timeTakenToTravelAtSellDestination >= 0) {
                        currentTime -= timeTakenToTravelAtSellDestination;
                        actionLines.add("B " + "0" + " " + amountToBuy);
                        ++actionsCount;
                    } else moveToNextBestCity = true;
                    //Traverse path to best place to sell
                    GraphPath<City, DefaultWeightedEdge> path = paths.getPath(mostProfitableSellPlace);
                    if(path == null) {
                        break;
                    }
                    List<City> verticesAlongPath = path.getVertexList();

                    for(int k = 1; k < verticesAlongPath.size(); ++k) {
                        actionLines.add("M " + verticesAlongPath.get(k).getId());
                        ++actionsCount;
                    }
                    //Sell products at destination
                    actionLines.add("S " + "0" + " " + amountToBuy);
                    ++actionsCount;
                    currentGold += amountToBuy * mostProfitableSellPlace.getSellPrice();

                    //Travel back to start to buy again if time allows it
                    if(currentTime - timeTakenToTravelAtSellDestination >= 0) {
                        currentTime -= timeTakenToTravelAtSellDestination;
                        for(int k = verticesAlongPath.size() - 2; k >= 0; --k) {
                            actionLines.add("M " + verticesAlongPath.get(k).getId());
                            ++actionsCount;
                        }
                    } else break;
                }

                writer.println(actionsCount);
                for (int l = 0; l < actionLines.size(); ++l) {
                    writer.println(actionLines.get(l));
                }
            }
            writer.close(); // close the PrintWriter object to flush the buffer and release the resources
        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
        }

    }
}
