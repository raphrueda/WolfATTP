/*
Algorithmic Trading Testing Platform Controller
Author: Raphael Rueda
Team: Wolf of SENG
 */

package attp;

import javafx.beans.property.SimpleDoubleProperty;
import javafx.concurrent.Service;
import javafx.concurrent.Task;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.geometry.Side;
import javafx.scene.Parent;
import javafx.scene.chart.*;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.shape.Rectangle;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.scene.input.MouseEvent;

import java.io.*;
import java.net.URL;
import java.util.*;

public class Controller implements Initializable {

    private String dataFile;
    private boolean alreadyRun;
    private ArrayList<String> orders = new ArrayList<>();
    Hashtable<String, ArrayList<ArrayList<String>>> data;
    ArrayList<String> companies;

    //=-=-=-=-= Profile globals =-=-=-=-=\\

    Hashtable<String, StackPane> companyProfiles;
    Hashtable<String, StackPane> companyMaps;
    XYChart.Series savedStockSeries;
    XYChart.Series savedVolumeSeries;

    StackPane currProfile;
    Rectangle profileSelection;
    SimpleDoubleProperty selectionInitX = new SimpleDoubleProperty();
    SimpleDoubleProperty selectionCurrX = new SimpleDoubleProperty();
    private boolean selectionMade;

    //=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\\

    //=-=-=-=-=-= Portfolio1  =-=-=-=-=-=\\

    XYChart.Series savedP1PositionSeries;
    XYChart.Series savedP1CashPositionSeries;

    Rectangle p1Selection;
    SimpleDoubleProperty p1SelectionInitX = new SimpleDoubleProperty();
    SimpleDoubleProperty p1SelectionCurrX = new SimpleDoubleProperty();

    String p1SelectedStrategy;
    String p1SelectedCompany;

    String p1SelectedFile;

    String p1EndCashPosition;
    String p1EndPosition;
    String p1Equity;

    //=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\\

    //=-=-=-=-=-= Portfolio2  =-=-=-=-=-=\\

    XYChart.Series savedP2PositionSeries;
    XYChart.Series savedP2CashPositionSeries;

    Rectangle p2Selection;
    SimpleDoubleProperty p2SelectionInitX = new SimpleDoubleProperty();
    SimpleDoubleProperty p2SelectionCurrX = new SimpleDoubleProperty();

    String p2SelectedStrategy;
    String p2SelectedCompany;

    String p2EndCashPosition;
    String p2EndPosition;
    String p2Equity;

    //=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\\

    //=-=-=-=-=-= Portfolio3  =-=-=-=-=-=\\

    XYChart.Series savedP3PositionSeries;
    XYChart.Series savedP3CashPositionSeries;

    Rectangle p3Selection;
    SimpleDoubleProperty p3SelectionInitX = new SimpleDoubleProperty();
    SimpleDoubleProperty p3SelectionCurrX = new SimpleDoubleProperty();

    String p3SelectedStrategy;
    String p3SelectedCompany;

    String p3EndCashPosition;
    String p3EndPosition;
    String p3Equity;

    //=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\\


    EventHandler<MouseEvent> selectionHandler = new EventHandler<MouseEvent>() {
        @Override
        public void handle(MouseEvent event) {
            if (event.getEventType() == MouseEvent.MOUSE_PRESSED) {
                selectionCurrX.set(0);
                profileSelection.setVisible(true);
                profileSelection.setX(Math.max(event.getX(), 70.0));
                profileSelection.setY(10);
                selectionInitX.set(event.getX());
            } else if (event.getEventType() == MouseEvent.MOUSE_DRAGGED) {
                selectionCurrX.set(Math.min(event.getX(), 943.0));
            } else if (event.getEventType() == MouseEvent.MOUSE_RELEASED) {
                if (selectionInitX.get() < selectionCurrX.get()){
                    double left = profileSelection.getX() - 70;
                    double right = profileSelection.getX() + profileSelection.getWidth() - 70;
                    double leftPercent = left/873;
                    double rightPercent = right/873;
                    BarChart<String, Number> volumeChart = (BarChart) currProfile.getChildren().get(0);
                    LineChart<String, Number> stockChart = (LineChart) currProfile.getChildren().get(1);

                    volumeChart.getData().clear();
                    stockChart.getData().clear();

                    XYChart.Series newVolumeSeries = new XYChart.Series();
                    XYChart.Series newStockSeries = new XYChart.Series();

                    int seriesSize = savedVolumeSeries.getData().size();
                    int leftRemove = (int) (seriesSize * leftPercent);
                    int rightRemove = (int) (seriesSize * rightPercent);
                    for (int i = 0; i < savedVolumeSeries.getData().size(); i++) {
                        if (leftRemove <= i && i <= rightRemove) {
                            XYChart.Data<String, Number> savedVolumePlot = (XYChart.Data<String, Number>) savedVolumeSeries.getData().get(i);
                            XYChart.Data newVolumePlot = new XYChart.Data(savedVolumePlot.getXValue(), savedVolumePlot.getYValue());
                            newVolumeSeries.getData().add(newVolumePlot);

                            XYChart.Data<String, Number> savedStockPlot = (XYChart.Data<String, Number>) savedStockSeries.getData().get(i);
                            XYChart.Data newStockPlot = new XYChart.Data(savedStockPlot.getXValue(), savedStockPlot.getYValue());
                            Rectangle rectangle1 = new Rectangle(0,0);
                            rectangle1.setVisible(false);
                            newStockPlot.setNode(rectangle1);
                            newStockSeries.getData().add(newStockPlot);
                        }
                        if (i > rightRemove) break;
                    }
                    volumeChart.getData().add(newVolumeSeries);
                    stockChart.getData().add(newStockSeries);
                    selectionMade = true;
                }
            }
        }
    };

    EventHandler<MouseEvent> p1SelectionHandler = new EventHandler<MouseEvent>() {
        @Override
        public void handle(MouseEvent event) {
            if (event.getEventType() == MouseEvent.MOUSE_PRESSED) {
                p1SelectionCurrX.set(0);
                p1Selection.setVisible(true);
                p1Selection.setX(Math.max(event.getX(), 40.0));
                p1Selection.setY(10);
                p1SelectionInitX.set(event.getX());
            } else if (event.getEventType() == MouseEvent.MOUSE_DRAGGED) {
                p1SelectionCurrX.set(Math.min(event.getX(), 879.0));
            } else if (event.getEventType() == MouseEvent.MOUSE_RELEASED) {
                if (p1SelectionInitX.get() < p1SelectionCurrX.get()){
                    double left = p1Selection.getX() - 40;
                    double right = p1Selection.getX() + p1Selection.getWidth() - 40;
                    double leftPercent = left/839;
                    double rightPercent = right/839;
                    BarChart<String, Number> positionChart = (BarChart) p1Position;
                    LineChart<String, Number> cashPositionChart = (LineChart) p1CashPosition;

                    positionChart.getData().clear();
                    cashPositionChart.getData().clear();

                    XYChart.Series newPositionSeries = new XYChart.Series();
                    XYChart.Series newCashPositionSeries = new XYChart.Series();

                    int seriesSize = savedP1PositionSeries.getData().size();
                    int leftRemove = (int) (seriesSize * leftPercent);
                    int rightRemove = (int) (seriesSize * rightPercent);
                    for (int i = 0; i < savedP1PositionSeries.getData().size(); i++) {
                        if (leftRemove <= i && i <= rightRemove) {
                            XYChart.Data<String, Number> savedPositionPlot = (XYChart.Data<String, Number>) savedP1PositionSeries.getData().get(i);
                            XYChart.Data newPositionPlot = new XYChart.Data(savedPositionPlot.getXValue(), savedPositionPlot.getYValue());
                            newPositionSeries.getData().add(newPositionPlot);

                            XYChart.Data<String, Number> savedCashPositionPlot = (XYChart.Data<String, Number>) savedP1CashPositionSeries.getData().get(i);
                            XYChart.Data newCashPositionPlot = new XYChart.Data(savedCashPositionPlot.getXValue(), savedCashPositionPlot.getYValue());
                            Rectangle rectangle1 = new Rectangle(0,0);
                            rectangle1.setVisible(false);
                            newCashPositionPlot.setNode(rectangle1);
                            newCashPositionSeries.getData().add(newCashPositionPlot);
                        }
                        if (i > rightRemove) break;
                    }
                    positionChart.getData().add(newPositionSeries);
                    cashPositionChart.getData().add(newCashPositionSeries);
                }
            }
        }
    };

    EventHandler<MouseEvent> p2SelectionHandler = new EventHandler<MouseEvent>() {
        @Override
        public void handle(MouseEvent event) {
            if (event.getEventType() == MouseEvent.MOUSE_PRESSED) {
                p2SelectionCurrX.set(0);
                p2Selection.setVisible(true);
                p2Selection.setX(Math.max(event.getX(), 40.0));
                p2Selection.setY(10);
                p2SelectionInitX.set(event.getX());
            } else if (event.getEventType() == MouseEvent.MOUSE_DRAGGED) {
                p2SelectionCurrX.set(Math.min(event.getX(), 879.0));
            } else if (event.getEventType() == MouseEvent.MOUSE_RELEASED) {
                if (p2SelectionInitX.get() < p2SelectionCurrX.get()){
                    double left = p2Selection.getX() - 40;
                    double right = p2Selection.getX() + p2Selection.getWidth() - 40;
                    double leftPercent = left/839;
                    double rightPercent = right/839;
                    BarChart<String, Number> positionChart = (BarChart) p2Position;
                    LineChart<String, Number> cashPositionChart = (LineChart) p2CashPosition;

                    positionChart.getData().clear();
                    cashPositionChart.getData().clear();

                    XYChart.Series newPositionSeries = new XYChart.Series();
                    XYChart.Series newCashPositionSeries = new XYChart.Series();

                    int seriesSize = savedP2PositionSeries.getData().size();
                    int leftRemove = (int) (seriesSize * leftPercent);
                    int rightRemove = (int) (seriesSize * rightPercent);
                    for (int i = 0; i < savedP2PositionSeries.getData().size(); i++) {
                        if (leftRemove <= i && i <= rightRemove) {
                            XYChart.Data<String, Number> savedPositionPlot = (XYChart.Data<String, Number>) savedP2PositionSeries.getData().get(i);
                            XYChart.Data newPositionPlot = new XYChart.Data(savedPositionPlot.getXValue(), savedPositionPlot.getYValue());
                            newPositionSeries.getData().add(newPositionPlot);

                            XYChart.Data<String, Number> savedCashPositionPlot = (XYChart.Data<String, Number>) savedP2CashPositionSeries.getData().get(i);
                            XYChart.Data newCashPositionPlot = new XYChart.Data(savedCashPositionPlot.getXValue(), savedCashPositionPlot.getYValue());
                            Rectangle rectangle1 = new Rectangle(0,0);
                            rectangle1.setVisible(false);
                            newCashPositionPlot.setNode(rectangle1);
                            newCashPositionSeries.getData().add(newCashPositionPlot);
                        }
                        if (i > rightRemove) break;
                    }
                    positionChart.getData().add(newPositionSeries);
                    cashPositionChart.getData().add(newCashPositionSeries);
                }
            }
        }
    };

    EventHandler<MouseEvent> p3SelectionHandler = new EventHandler<MouseEvent>() {
        @Override
        public void handle(MouseEvent event) {
            if (event.getEventType() == MouseEvent.MOUSE_PRESSED) {
                p3SelectionCurrX.set(0);
                p3Selection.setVisible(true);
                p3Selection.setX(Math.max(event.getX(), 40.0));
                p3Selection.setY(10);
                p3SelectionInitX.set(event.getX());
            } else if (event.getEventType() == MouseEvent.MOUSE_DRAGGED) {
                p3SelectionCurrX.set(Math.min(event.getX(), 879.0));
            } else if (event.getEventType() == MouseEvent.MOUSE_RELEASED) {
                if (p3SelectionInitX.get() < p3SelectionCurrX.get()){
                    double left = p3Selection.getX() - 40;
                    double right = p3Selection.getX() + p3Selection.getWidth() - 40;
                    double leftPercent = left/839;
                    double rightPercent = right/839;
                    BarChart<String, Number> positionChart = (BarChart) p3Position;
                    LineChart<String, Number> cashPositionChart = (LineChart) p3CashPosition;

                    positionChart.getData().clear();
                    cashPositionChart.getData().clear();

                    XYChart.Series newPositionSeries = new XYChart.Series();
                    XYChart.Series newCashPositionSeries = new XYChart.Series();

                    int seriesSize = savedP3PositionSeries.getData().size();
                    int leftRemove = (int) (seriesSize * leftPercent);
                    int rightRemove = (int) (seriesSize * rightPercent);
                    for (int i = 0; i < savedP3PositionSeries.getData().size(); i++) {
                        if (leftRemove <= i && i <= rightRemove) {
                            XYChart.Data<String, Number> savedPositionPlot = (XYChart.Data<String, Number>) savedP3PositionSeries.getData().get(i);
                            XYChart.Data newPositionPlot = new XYChart.Data(savedPositionPlot.getXValue(), savedPositionPlot.getYValue());
                            newPositionSeries.getData().add(newPositionPlot);

                            XYChart.Data<String, Number> savedCashPositionPlot = (XYChart.Data<String, Number>) savedP3CashPositionSeries.getData().get(i);
                            XYChart.Data newCashPositionPlot = new XYChart.Data(savedCashPositionPlot.getXValue(), savedCashPositionPlot.getYValue());
                            Rectangle rectangle1 = new Rectangle(0,0);
                            rectangle1.setVisible(false);
                            newCashPositionPlot.setNode(rectangle1);
                            newCashPositionSeries.getData().add(newCashPositionPlot);
                        }
                        if (i > rightRemove) break;
                    }
                    positionChart.getData().add(newPositionSeries);
                    cashPositionChart.getData().add(newCashPositionSeries);
                }
            }
        }
    };

    @FXML Parent root;

    //Step 1
    @FXML Button openBtn;
    @FXML Button loadBtn;
    @FXML Label dataPath;
    @FXML ProgressIndicator profileProgress;

    //Step 2
    @FXML TextField startInput;
    @FXML TextField endInput;
    @FXML ChoiceBox<String> strategy1;
    @FXML TextField nInput1;
    @FXML TextField thInput1;
    @FXML ChoiceBox<String> strategy2;
    @FXML TextField nInput2;
    @FXML TextField thInput2;

    //Step 3
    @FXML Button runBtn;
    @FXML Button reportBtn;
    @FXML Button csvBtn;
    @FXML ProgressIndicator progress;

    //Stage
    @FXML TabPane tabPane;
    @FXML Tab tab1;
    @FXML Tab tab2;
    @FXML VBox portfolioStage;

    //Portfolio1 Objects
    @FXML VBox portfolio1;
    @FXML ChoiceBox p1StrategySelector;
    @FXML ChoiceBox p1CompanySelector;
    @FXML TextField p1Initial;
    @FXML Button p1RunBtn;
    @FXML BarChart p1Position;
    @FXML LineChart p1CashPosition;
    @FXML BarChart p1PositionMap;
    @FXML LineChart p1CashPositionMap;
    @FXML StackPane p1Nav;
    @FXML ProgressIndicator p1Indicator;
    @FXML Label p1EndCashPositionLbl;
    @FXML Label p1EndPositionLbl;
    @FXML Label p1EquityLbl;

    //Portfolio2 Objects
    @FXML VBox portfolio2;
    @FXML ChoiceBox p2StrategySelector;
    @FXML ChoiceBox p2CompanySelector;
    @FXML TextField p2Initial;
    @FXML Button p2RunBtn;
    @FXML BarChart p2Position;
    @FXML LineChart p2CashPosition;
    @FXML BarChart p2PositionMap;
    @FXML LineChart p2CashPositionMap;
    @FXML StackPane p2Nav;
    @FXML ProgressIndicator p2Indicator;
    @FXML Label p2EndCashPositionLbl;
    @FXML Label p2EndPositionLbl;
    @FXML Label p2EquityLbl;

    //Portfolio3 Objects
    @FXML VBox portfolio3;
    @FXML ChoiceBox p3StrategySelector;
    @FXML ChoiceBox p3CompanySelector;
    @FXML TextField p3Initial;
    @FXML Button p3RunBtn;
    @FXML BarChart p3Position;
    @FXML LineChart p3CashPosition;
    @FXML BarChart p3PositionMap;
    @FXML LineChart p3CashPositionMap;
    @FXML StackPane p3Nav;
    @FXML ProgressIndicator p3Indicator;
    @FXML Label p3EndCashPositionLbl;
    @FXML Label p3EndPositionLbl;
    @FXML Label p3EquityLbl;

    public Controller() {
    }

    /**
     * Code that runs at the very start of the application
     */
    @Override
    public void initialize(URL location, ResourceBundle resources) {
        //Add listener to the first strategy drop down
        strategy1.setValue("Wolf of SENG");
        strategy1.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    if (newValue.equals("WilliamsR")){
                        thInput1.setDisable(true);
                    } else {
                        thInput1.setDisable(false);
                    }
                }
        );
        //Add listener to the first strategy drop down
        strategy2.setValue("(optional)");
        strategy2.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    if (newValue.equals("WilliamsR")){
                        thInput2.setDisable(true);
                    } else {
                        thInput2.setDisable(false);
                    }
                }
        );
        alreadyRun = false;
        selectionMade = false;
    }

    /**
     * Opens the file chooser
     * Tied to 'openBtn' through FXML
     */
    public void openBtnClicked(){
        Stage stage = (Stage) root.getScene().getWindow();

        FileChooser chooser = new FileChooser();
        chooser.setTitle("Choose Data File");
        File file = chooser.showOpenDialog(stage);
        //If file successfully chosen save its name/path
        if(file != null) {
            dataPath.setText(file.getName());
            dataFile = file.getAbsolutePath();
            //Allow use of the load button
            loadBtn.setDisable(false);
        }
    }

    /**
     * Analyses a valid data file and creates a profile for each company
     * Tied to 'loadBtn' through FXML
     */
    public void loadBtnClicked() throws IOException {

        //Service that populates the company profile tab
        final Service<VBox> mainStageBuilder = new Service<VBox>() {
            @Override protected Task<VBox> createTask() {
                return new Task<VBox>() {
                    @Override protected VBox call() throws Exception {
                        //Send service progress update to activate indicator
                        updateProgress(0,10);
                        VBox mainStage = new VBox(5);
                        mainStage.setPadding(new Insets(10, 10, 10, 10));

                        //Open data file
                        BufferedReader reader = new BufferedReader(new FileReader(dataFile));
                        String currLine = reader.readLine();

                        //Check for valid data file header
                        if (currLine.equals("#RIC,Date[L],Time[L],Type,Qualifiers,Open,High,Low,Last,Volume,Open Interest,Settle,Data Source")) {
                            //Store company names
                            companies = new ArrayList<>();

                            //Store company data in a 2D Array List
                            Hashtable<String, ArrayList<ArrayList<String>>> testList = new Hashtable<>();

                            while ((currLine = reader.readLine()) != null) {
                                String[] fields = currLine.split(",");
                                if (fields[4].equals("No Trade") || fields[8].equals("")) {
                                    continue;
                                } else {
                                    //Date, Last and Volume
                                    ArrayList<String> currData = new ArrayList<String>();
                                    currData.add(fields[1]); //Add Date
                                    currData.add(fields[8]); //Add Last Val
                                    currData.add(fields[9]); //Add Volume
                                    if (testList.get(fields[0]) == null) {
                                        testList.put(fields[0], new ArrayList<>());
                                        companies.add(fields[0]);
                                    }
                                    testList.get(fields[0]).add(currData);
                                }
                            }
                            data = testList;
                            reader.close();

                            //Construct company drop down
                            ChoiceBox<String> companySelector = new ChoiceBox<>();

                            //Store the company graphs/navigation maps
                            companyProfiles = new Hashtable<>();
                            companyMaps = new Hashtable<>();

                            //Create the company graphs/navigation maps and add them to their respective pane
                            StackPane profile = new StackPane();
                            StackPane map = new StackPane();
                            for (String company : companies) {
                                companySelector.getItems().add(company);
                                companyProfiles.put(company, makeCompanyProfile(company));
                                companyMaps.put(company, makeCompanyMap(company));
                                profile.getChildren().add(companyProfiles.get(company));
                                map.getChildren().add(companyMaps.get(company));
                            }

                            //Hack-y visuals
                            Rectangle volumeLegend = new Rectangle(15, 15);
                            volumeLegend.setStrokeWidth(0);
                            volumeLegend.setArcHeight(0);
                            volumeLegend.setArcWidth(0);
                            volumeLegend.setTranslateX(-455);
                            volumeLegend.setTranslateY(0);
                            volumeLegend.setFill(Paint.valueOf("#ed591a"));

                            Rectangle priceLegend = new Rectangle(15, 15);
                            priceLegend.setStrokeWidth(0);
                            priceLegend.setArcHeight(0);
                            priceLegend.setArcWidth(0);
                            priceLegend.setTranslateX(455);
                            priceLegend.setTranslateY(5);
                            priceLegend.setFill(Paint.valueOf("#487aae"));

                            profile.getChildren().addAll(volumeLegend, priceLegend);

                            //Set up the profile navigation selection
                            profileSelection = new Rectangle();
                            profileSelection.setFill(Color.web("blue", 0.1));
                            profileSelection.setStroke(Color.BLUE);
                            profileSelection.setStrokeDashOffset(50);

                            profileSelection.widthProperty().bind(selectionCurrX.subtract(selectionInitX));
                            profileSelection.heightProperty().setValue(55);
                            profileSelection.setVisible(false);

                            //Tie listener to navigation(selection) pane
                            BorderPane selectionPane = new BorderPane();
                            selectionPane.setOnMouseClicked(selectionHandler);
                            selectionPane.setOnMouseDragged(selectionHandler);
                            selectionPane.setOnMouseEntered(selectionHandler);
                            selectionPane.setOnMouseExited(selectionHandler);
                            selectionPane.setOnMouseMoved(selectionHandler);
                            selectionPane.setOnMousePressed(selectionHandler);
                            selectionPane.setOnMouseReleased(selectionHandler);

                            selectionPane.getChildren().add(profileSelection);
                            map.getChildren().add(selectionPane);

                            //Piecing elements together
                            HBox companyChoiceContainer = new HBox(10);
                            companyChoiceContainer.setAlignment(Pos.CENTER_LEFT);
                            companyChoiceContainer.getChildren().add(new Label("Company: "));
                            companyChoiceContainer.getChildren().add(companySelector);
                            mainStage.getChildren().add(companyChoiceContainer);
                            mainStage.getChildren().add(profile);
                            mainStage.getChildren().add(new Separator());
                            mainStage.getChildren().add(new Label("Navigation"));
                            mainStage.getChildren().add(map);

                            //Set default values
                            if (companies.get(0) != null) {
                                companySelector.setValue(companies.get(0));
                                companyProfiles.get(companies.get(0)).setVisible(true);
                                companyMaps.get(companies.get(0)).setVisible(true);
                                currProfile = companyProfiles.get(companies.get(0));
                                BarChart<String, Number> tempVolume = (BarChart) currProfile.getChildren().get(0);
                                savedVolumeSeries = tempVolume.getData().get(0);
                                LineChart<String, Number> tempStock = (LineChart) currProfile.getChildren().get(1);
                                savedStockSeries = (XYChart.Series) tempStock.getData().get(0);
                            }

                            //Create company drop down listener
                            companySelector.getSelectionModel().selectedItemProperty().addListener(
                                    (v, oldValue, newValue) -> {
                                        if (selectionMade == true) {
                                            BarChart<String, Number> restoreVolume = (BarChart) currProfile.getChildren().get(0);
                                            restoreVolume.getData().clear();
                                            restoreVolume.getData().add(savedVolumeSeries);

                                            LineChart<String, Number> restoreStock = (LineChart) currProfile.getChildren().get(1);
                                            restoreStock.getData().clear();
                                            restoreStock.getData().add(savedStockSeries);
                                        }

                                        profileSelection.setVisible(false);

                                        companyProfiles.get(oldValue).setVisible(false);
                                        companyProfiles.get(newValue).setVisible(true);
                                        companyMaps.get(oldValue).setVisible(false);
                                        companyMaps.get(newValue).setVisible(true);
                                        currProfile = companyProfiles.get(newValue);
                                        BarChart<String, Number> tempVolume = (BarChart) currProfile.getChildren().get(0);
                                        savedVolumeSeries = tempVolume.getData().get(0);
                                        LineChart<String, Number> tempStock = (LineChart) currProfile.getChildren().get(1);
                                        savedStockSeries = (XYChart.Series) tempStock.getData().get(0);
                                        selectionMade = false;
                                    }
                            );
                        } else {
                            this.cancel();
                        }
                        return mainStage;
                    }
                };
            }
        };

        mainStageBuilder.stateProperty().addListener((v, oldState, newState) -> {
            switch (newState) {
                case SCHEDULED:
                    System.out.println("scheduled");
                    break;
                case READY:
                    System.out.println("ready");
                case RUNNING:
                    break;
                case SUCCEEDED:
                    System.out.println("succeeded");
                    profileProgress.visibleProperty().unbind();
                    profileProgress.setVisible(false);
                    //Pull the stage from the service and add it to the window
                    VBox mainStage = mainStageBuilder.valueProperty().getValue();
                    tab1.setContent(mainStage);
                    tabPane.getSelectionModel().select(0);
                    tab2.setDisable(true);
                    runBtn.setDisable(false);
                    break;
                case CANCELLED:
                    //Catch when stage building was cancelled
                    System.out.println("cancelled");
                    profileProgress.visibleProperty().unbind();
                    profileProgress.setVisible(false);
                    AlertBox.display("Invalid File", "Please make sure valid file was given.");
                    break;
                case FAILED:
                    //Catch when stage building failed
                    System.out.println("failed");
                    profileProgress.visibleProperty().unbind();
                    profileProgress.setVisible(false);
                    AlertBox.display("Error", "Something went wrong. Please try again.");
                    break;
            }
        });

        profileProgress.visibleProperty().bind(mainStageBuilder.progressProperty().isNotEqualTo(new SimpleDoubleProperty(ProgressBar.INDETERMINATE_PROGRESS)));
        mainStageBuilder.restart();
    }

    /**
     * Creates a company's profile (volume vs stock price vs time)
     * @param company String of the company
     * @return Stackpane containing 2 layered graphs
     */
    public StackPane makeCompanyProfile(String company){
        ArrayList<ArrayList<String>> companyData = data.get(company);

        //Construct the graphs
        CategoryAxis xAxis1 = new CategoryAxis();
        NumberAxis yAxis1 = new NumberAxis();
        LineChart<String, Number> stockPrice = new LineChart<>(xAxis1,yAxis1);

        CategoryAxis xAxis2 = new CategoryAxis();
        NumberAxis yAxis2 = new NumberAxis();
        xAxis2.setAnimated(false);
        BarChart<String, Number> volume = new BarChart<>(xAxis2, yAxis2);

        XYChart.Series series1 = new XYChart.Series();
        XYChart.Series series2 = new XYChart.Series();

        //Populate the series (volume and stock price)
        for (ArrayList<String> day : companyData) {
            XYChart.Data plot1 = new XYChart.Data(day.get(0), Double.parseDouble(day.get(1)));
            Rectangle rectangle1 = new Rectangle(0,0);
            rectangle1.setVisible(false);
            plot1.setNode(rectangle1);
            series1.getData().add(plot1);
            XYChart.Data plot2 = new XYChart.Data(day.get(0), Double.parseDouble(day.get(2)));
            series2.getData().add(plot2);
        }

        //Stock Price visual settings
        stockPrice.getData().add(series1);
        stockPrice.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());
        stockPrice.setLegendVisible(false);
        stockPrice.setAlternativeRowFillVisible(false);
        stockPrice.setAlternativeColumnFillVisible(false);
        stockPrice.setHorizontalGridLinesVisible(false);
        stockPrice.setVerticalGridLinesVisible(false);
        stockPrice.setHorizontalZeroLineVisible(false);
        stockPrice.setVerticalZeroLineVisible(false);
        stockPrice.getXAxis().setOpacity(0);
        stockPrice.getYAxis().setSide(Side.RIGHT);
        stockPrice.getYAxis().setMinWidth(50);
        stockPrice.getYAxis().setPrefWidth(50);
        stockPrice.getYAxis().setMaxWidth(50);
        stockPrice.setPadding(new Insets(0, 0, 0, 80));
        stockPrice.getYAxis().setLabel("Stock Price");

        //Volume visual settings
        volume.getData().add(series2);
        volume.getStylesheets().addAll(getClass().getResource("barCharts.css").toExternalForm());
        volume.setLegendVisible(false);
        volume.getYAxis().setMinWidth(80);
        volume.getYAxis().setPrefWidth(80);
        volume.getYAxis().setMaxWidth(80);
        volume.setPadding(new Insets(0, 50, 0, 0));
        volume.getYAxis().setLabel("Volume");

        //Combine graphs and return the pane
        StackPane profile = new StackPane();
        profile.getChildren().add(volume);
        profile.getChildren().add(stockPrice);
        profile.setPadding(new Insets(0, 30, 0, 30));
        profile.setVisible(false);
        return profile;
    }

    /**
     * Creates a navigation for the respective profile
     * @param company String of the company
     * @return Stackpane containing 2 shorter layered graphs
     */
    public StackPane makeCompanyMap(String company){
        ArrayList<ArrayList<String>> companyData = data.get(company);

        //Construct the graphs
        CategoryAxis xAxis1 = new CategoryAxis();
        NumberAxis yAxis1 = new NumberAxis();
        LineChart<String, Number> stockPrice = new LineChart<>(xAxis1,yAxis1);

        CategoryAxis xAxis2 = new CategoryAxis();
        NumberAxis yAxis2 = new NumberAxis();
        BarChart<String, Number> volume = new BarChart<>(xAxis2, yAxis2);

        XYChart.Series series1 = new XYChart.Series();
        XYChart.Series series2 = new XYChart.Series();

        //Populate the series
        for (ArrayList<String> day : companyData) {
            XYChart.Data plot1 = new XYChart.Data(day.get(0), Double.parseDouble(day.get(1)));
            Rectangle rectangle1 = new Rectangle(0,0);
            rectangle1.setVisible(false);
            plot1.setNode(rectangle1);
            series1.getData().add(plot1);
            XYChart.Data plot2 = new XYChart.Data(day.get(0), Double.parseDouble(day.get(2)));
            series2.getData().add(plot2);
        }

        //Stock Price settings
        stockPrice.getData().add(series1);
        stockPrice.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());
        stockPrice.setLegendVisible(false);
        stockPrice.setAlternativeRowFillVisible(false);
        stockPrice.setAlternativeColumnFillVisible(false);
        stockPrice.setHorizontalGridLinesVisible(false);
        stockPrice.setVerticalGridLinesVisible(false);
        stockPrice.setHorizontalZeroLineVisible(false);
        stockPrice.setVerticalZeroLineVisible(false);
        stockPrice.getXAxis().setOpacity(0);
        stockPrice.getYAxis().setOpacity(0);
        stockPrice.getYAxis().setMinWidth(30);
        stockPrice.getYAxis().setPrefWidth(30);
        stockPrice.getYAxis().setMaxWidth(30);
        stockPrice.getXAxis().setMinHeight(0);
        stockPrice.getXAxis().setPrefHeight(0);
        stockPrice.getXAxis().setMaxHeight(0);
        stockPrice.setPadding(new Insets(0, 30, 0, 0));
        stockPrice.setMinHeight(75);
        stockPrice.setPrefHeight(75);
        stockPrice.setMaxHeight(75);

        //Volume settings
        volume.getData().add(series2);
        volume.getStylesheets().addAll(getClass().getResource("mapBarCharts.css").toExternalForm());
        volume.setLegendVisible(false);
        volume.setAlternativeRowFillVisible(false);
        volume.setAlternativeColumnFillVisible(false);
        volume.setHorizontalGridLinesVisible(false);
        volume.setVerticalGridLinesVisible(false);
        volume.setHorizontalZeroLineVisible(false);
        volume.setVerticalZeroLineVisible(false);
        volume.getXAxis().setOpacity(0);
        volume.getYAxis().setOpacity(0);
        volume.getYAxis().setMinWidth(30);
        volume.getYAxis().setPrefWidth(30);
        volume.getYAxis().setMaxWidth(30);
        volume.getXAxis().setMinHeight(0);
        volume.getXAxis().setPrefHeight(0);
        volume.getXAxis().setMaxHeight(0);
        volume.setPadding(new Insets(0, 30, 0, 0));
        volume.setMinHeight(75);
        volume.setPrefHeight(75);
        volume.setMaxHeight(75);

        //Combine and return
        StackPane map = new StackPane();
        map.getChildren().add(volume);
        map.getChildren().add(stockPrice);
        map.setPadding(new Insets(0, 30, 0, 30));
        map.setVisible(false);
        return map;
    }

    /**
     * Sanitises data and runs the interface if data is valid
     * Creates a summary graph of the orders made
     * Tied to 'runBtn' through FXML
     */
    public void runBtnClicked() throws IOException, InterruptedException {
        //Service to call the python modules
        Service<ArrayList<String>> runService = new Service<ArrayList<String>>() {
            @Override protected Task<ArrayList<String>> createTask() {
                return new Task<ArrayList<String>>() {
                    @Override protected ArrayList<String> call() throws Exception {
                        //ArrayList to hold the orders files generated by python modules
                        ArrayList<String> ordersFiles = new ArrayList<>();
                        updateProgress(0,10);
                        if(alreadyRun == false) {
                            if (handleData()) {
                                //Start Wayne's interface
                                ProcessBuilder pb = new ProcessBuilder("python", "javaToPyInterface.py");
                                pb.redirectErrorStream(true);
                                Process process = pb.start();
                                //Pause thread until interface is done
                                process.waitFor();

                                //Pull output from Wayne's interface (names of order files)
                                InputStream is = process.getInputStream();
                                InputStreamReader isr = new InputStreamReader(is);
                                BufferedReader br = new BufferedReader(isr);

                                //Add the names of each orders file to a list
                                String line;
                                while ((line = br.readLine()) != null) {
                                    ordersFiles.add(line);
                                }
                                return ordersFiles;
                            }
                        } else {
                            boolean answer = ConfirmBox.display("Alert", "Continue? You will lose existing data");
                            if(answer){
                                alreadyRun = false;
                                runBtnClicked();
                            }
                        }
                        return null;
                    }
                };
            }
        };

        runService.stateProperty().addListener((v, oldState, newState) -> {
            switch (newState) {
                case SCHEDULED:
                    break;
                case READY:
                case RUNNING:
                    break;
                case SUCCEEDED:
                    //Clear profiles
                    p1StrategySelector.getItems().clear();
                    p2StrategySelector.getItems().clear();
                    p3StrategySelector.getItems().clear();
                    p1CompanySelector.getItems().clear();
                    p2CompanySelector.getItems().clear();
                    p3CompanySelector.getItems().clear();

                    p1Position.getData().clear();
                    p1CashPosition.getData().clear();
                    p2Position.getData().clear();
                    p2CashPosition.getData().clear();
                    p3Position.getData().clear();
                    p3CashPosition.getData().clear();
                    p1PositionMap.getData().clear();
                    p1CashPositionMap.getData().clear();
                    p2PositionMap.getData().clear();
                    p2CashPositionMap.getData().clear();
                    p3PositionMap.getData().clear();
                    p3CashPositionMap.getData().clear();

                    progress.visibleProperty().unbind();
                    progress.setVisible(false);
                    orders = runService.valueProperty().getValue();

                    reportBtn.setDisable(false);
                    csvBtn.setDisable(false);
                    tab2.setDisable(false);

                    populatePortfolio();

                    tabPane.getSelectionModel().select(1);
                    alreadyRun = true;
                    break;
                case CANCELLED:
                    break;
                case FAILED:
                    progress.visibleProperty().unbind();
                    progress.setVisible(false);
                    boolean answer = ConfirmBox.display("Alert", "Continue? You will lose existing data");
                    if(answer){
                        alreadyRun = false;
                        try {
                            runBtnClicked();
                        } catch (IOException e) {
                            e.printStackTrace();
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                    break;
            }
        });

        progress.visibleProperty().bind(runService.progressProperty().isNotEqualTo(new SimpleDoubleProperty(ProgressBar.INDETERMINATE_PROGRESS)));
        runService.restart();
    }

    /**
     * Fill dropdown boxes in the portfolio
     * Called after ordersfiles are made
     */
    private void populatePortfolio() {
        for (String order : orders){
            p1StrategySelector.getItems().add(order);
            p2StrategySelector.getItems().add(order);
            p3StrategySelector.getItems().add(order);
        }
        p1StrategySelector.getSelectionModel().select(0);
        p1SelectedStrategy = (String) p1StrategySelector.getValue();
        p2StrategySelector.getSelectionModel().select(0);
        p2SelectedStrategy = (String) p2StrategySelector.getValue();
        p3StrategySelector.getSelectionModel().select(0);
        p3SelectedStrategy = (String) p3StrategySelector.getValue();
        p1StrategySelector.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    p1SelectedStrategy = (String) newValue;
                }
        );
        p2StrategySelector.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    p2SelectedStrategy = (String) newValue;
                }
        );
        p3StrategySelector.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    p3SelectedStrategy = (String) newValue;
                }
        );

        for (String company : companies){
            p1CompanySelector.getItems().add(company);
            p2CompanySelector.getItems().add(company);
            p3CompanySelector.getItems().add(company);
        }
        p1CompanySelector.getSelectionModel().select(0);
        p1SelectedCompany = (String) p1CompanySelector.getValue();
        p2CompanySelector.getSelectionModel().select(0);
        p2SelectedCompany = (String) p2CompanySelector.getValue();
        p3CompanySelector.getSelectionModel().select(0);
        p3SelectedCompany = (String) p3CompanySelector.getValue();
        p1CompanySelector.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    p1SelectedCompany = (String) newValue;
                }
        );
        p2CompanySelector.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    p2SelectedCompany = (String) newValue;
                }
        );
        p3CompanySelector.getSelectionModel().selectedItemProperty().addListener(
                (v, oldValue, newValue) -> {
                    p3SelectedCompany = (String) newValue;
                }
        );
    }

    /**
     * Creates the portfolio for a given strategy, company and initial investment
     * First portfolio
     * @throws IOException
     * @throws InterruptedException
     */
    public void p1RunBtnClicked() throws IOException, InterruptedException {
        if(!p1Initial.getText().isEmpty()){
            //Call python profiler module
            ProcessBuilder pb = new ProcessBuilder("python", "profiler.py",
                                                    p1SelectedStrategy,
                                                    p1Initial.getText(),
                                                    p1SelectedCompany);
            pb.redirectErrorStream(true);
            Process process = pb.start();
            process.waitFor();

            InputStream is = process.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);

            String line;
            while ((line = br.readLine()) != null) {
                p1SelectedFile = line;
            }

            //Set up profile graphs
            p1Position.getXAxis().setAnimated(false);
            p1Position.getStylesheets().addAll(getClass().getResource("barCharts.css").toExternalForm());
            p1CashPosition.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());
            p1PositionMap.getStylesheets().addAll(getClass().getResource("mapBarCharts.css").toExternalForm());
            p1CashPositionMap.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());

            //service to create series (4 total)
            final Service<ArrayList<XYChart.Series>> p1SeriesPopulator = new Service<ArrayList<XYChart.Series>>() {
                @Override protected Task<ArrayList<XYChart.Series>> createTask() {
                    return new Task<ArrayList<XYChart.Series>>() {
                        @Override protected ArrayList<XYChart.Series> call() throws Exception {
                            updateProgress(0, 10);
                            ArrayList<XYChart.Series> seriesList = new ArrayList<>();
                            BufferedReader reader = new BufferedReader(new FileReader(p1SelectedFile));
                            String currLine;
                            XYChart.Series positionSeries = new XYChart.Series();
                            XYChart.Series positionMapSeries = new XYChart.Series();
                            XYChart.Series cashPositionSeries = new XYChart.Series();
                            XYChart.Series cashPositionMapSeries = new XYChart.Series();
                            while((currLine = reader.readLine()) != null){
                                currLine = currLine.replaceAll("'", "");
                                if(currLine.contains("[")){
                                    currLine = currLine.replace("[", "");
                                    currLine = currLine.replace("]", "");
                                    String[] fields = currLine.split(",");
                                    p1EndCashPosition = fields[0];
                                    p1EndPosition = fields[1];
                                    p1Equity = fields[2];
                                } else {
                                    String[] fields = currLine.split(",");

                                    XYChart.Data positionPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[1]));
                                    positionSeries.getData().add(positionPlot);

                                    XYChart.Data positionMapPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[1]));
                                    positionMapSeries.getData().add(positionMapPlot);

                                    XYChart.Data cashPositionPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[0]));
                                    Rectangle rectangle1 = new Rectangle(0, 0);
                                    rectangle1.setVisible(false);
                                    cashPositionPlot.setNode(rectangle1);
                                    cashPositionSeries.getData().add(cashPositionPlot);

                                    XYChart.Data cashPositionMapPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[0]));
                                    Rectangle rectangle2 = new Rectangle(0, 0);
                                    rectangle2.setVisible(false);
                                    cashPositionMapPlot.setNode(rectangle2);
                                    cashPositionMapSeries.getData().add(cashPositionMapPlot);
                                }
                            }
                            savedP1PositionSeries = positionSeries;
                            savedP1CashPositionSeries = cashPositionSeries;
                            seriesList.add(positionSeries);
                            seriesList.add(positionMapSeries);
                            seriesList.add(cashPositionSeries);
                            seriesList.add(cashPositionMapSeries);
                            return seriesList;
                        }
                    };
                }
            };

            p1SeriesPopulator.stateProperty().addListener((v, oldState, newState) -> {
                switch (newState) {
                    case SCHEDULED:
                        System.out.println("scheduled");
                        break;
                    case READY:
                        System.out.println("ready");
                    case RUNNING:
                        break;
                    case SUCCEEDED:
                        //Populate profile 1
                        p1Indicator.visibleProperty().unbind();
                        p1Indicator.setVisible(false);
                        p1Position.getData().clear();
                        p1CashPosition.getData().clear();
                        p1PositionMap.getData().clear();
                        p1CashPositionMap.getData().clear();
                        ArrayList<XYChart.Series> series = p1SeriesPopulator.valueProperty().getValue();
                        p1Position.getData().add(series.get(0));
                        p1PositionMap.getData().add(series.get(1));
                        p1CashPosition.getData().add(series.get(2));
                        p1CashPositionMap.getData().add(series.get(3));
                        p1EndCashPositionLbl.setText(p1EndCashPosition);
                        p1EndPositionLbl.setText(p1EndPosition);
                        p1EquityLbl.setText(p1Equity);
                        break;
                    case CANCELLED:
                        break;
                    case FAILED:
                        break;
                }
            });

            //Service for navigation selector
            Service<BorderPane> p1SelectionPopulator =  new Service<BorderPane>() {
                @Override protected Task<BorderPane> createTask() {
                    return new Task<BorderPane>() {
                        @Override protected BorderPane call() throws Exception {
                            p1Selection = new Rectangle();
                            p1Selection.setFill(Color.web("blue", 0.1));
                            p1Selection.setStroke(Color.BLUE);
                            p1Selection.setStrokeDashOffset(50);

                            p1Selection.widthProperty().bind(p1SelectionCurrX.subtract(p1SelectionInitX));
                            p1Selection.heightProperty().setValue(55);
                            p1Selection.setVisible(false);

                            BorderPane p1SelectionPane = new BorderPane();

                            p1SelectionPane.setOnMouseClicked(p1SelectionHandler);
                            p1SelectionPane.setOnMouseDragged(p1SelectionHandler);
                            p1SelectionPane.setOnMouseEntered(p1SelectionHandler);
                            p1SelectionPane.setOnMouseExited(p1SelectionHandler);
                            p1SelectionPane.setOnMouseMoved(p1SelectionHandler);
                            p1SelectionPane.setOnMousePressed(p1SelectionHandler);
                            p1SelectionPane.setOnMouseReleased(p1SelectionHandler);

                            p1SelectionPane.getChildren().add(p1Selection);
                            return p1SelectionPane;
                        }
                    };
                }
            };

            p1SelectionPopulator.stateProperty().addListener((v, oldState, newState) -> {
                switch (newState) {
                    case SCHEDULED:
                        System.out.println("scheduled");
                        break;
                    case READY:
                        System.out.println("ready");
                    case RUNNING:
                        break;
                    case SUCCEEDED:
                        BorderPane selectionPane = p1SelectionPopulator.valueProperty().getValue();
                        p1Nav.getChildren().add(selectionPane);
                        break;
                    case CANCELLED:
                        break;
                    case FAILED:
                        break;
                }
            });

            p1Indicator.visibleProperty().bind(p1SeriesPopulator.progressProperty().isNotEqualTo(new SimpleDoubleProperty(ProgressBar.INDETERMINATE_PROGRESS)));
            p1SeriesPopulator.restart();
            p1SelectionPopulator.restart();

        } else {
            AlertBox.display("Missing Field", "Initial investment field is required");
        }
    }

    /**
     * Creates the portfolio for a given strategy, company and initial investment
     * Second portfolio
     * @throws IOException
     * @throws InterruptedException
     */
    public void p2RunBtnClicked() throws IOException, InterruptedException {
        if(!p2Initial.getText().isEmpty()){

            ProcessBuilder pb = new ProcessBuilder("python", "profiler.py",
                                                    p2SelectedStrategy,
                                                    p2Initial.getText(),
                                                    p2SelectedCompany);
            pb.redirectErrorStream(true);
            Process process = pb.start();
            process.waitFor();

            InputStream is = process.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);

            String p2FileName = "";
            String line;
            while ((line = br.readLine()) != null) {
                p2FileName = line;
            }

            p2Position.getXAxis().setAnimated(false);
            p2Position.getStylesheets().addAll(getClass().getResource("barCharts.css").toExternalForm());
            p2CashPosition.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());
            p2PositionMap.getStylesheets().addAll(getClass().getResource("mapBarCharts.css").toExternalForm());
            p2CashPositionMap.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());

            //service to create series (4 total)
            final String finalP2FileName = p2FileName;
            final Service<ArrayList<XYChart.Series>> p2SeriesPopulator = new Service<ArrayList<XYChart.Series>>() {
                @Override protected Task<ArrayList<XYChart.Series>> createTask() {
                    return new Task<ArrayList<XYChart.Series>>() {
                        @Override protected ArrayList<XYChart.Series> call() throws Exception {
                            updateProgress(0, 10);
                            ArrayList<XYChart.Series> seriesList = new ArrayList<>();
                            BufferedReader reader = new BufferedReader(new FileReader(finalP2FileName));
                            String currLine;
                            XYChart.Series positionSeries = new XYChart.Series();
                            XYChart.Series positionMapSeries = new XYChart.Series();
                            XYChart.Series cashPositionSeries = new XYChart.Series();
                            XYChart.Series cashPositionMapSeries = new XYChart.Series();
                            while((currLine = reader.readLine()) != null){
                                currLine = currLine.replaceAll("'", "");
                                if(currLine.contains("[")){
                                    currLine = currLine.replace("[", "");
                                    currLine = currLine.replace("]", "");
                                    String[] fields = currLine.split(",");
                                    p2EndCashPosition = fields[0];
                                    p2EndPosition = fields[1];
                                    p2Equity = fields[2];
                                } else {
                                    String[] fields = currLine.split(",");

                                    XYChart.Data positionPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[1]));
                                    positionSeries.getData().add(positionPlot);

                                    XYChart.Data positionMapPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[1]));
                                    positionMapSeries.getData().add(positionMapPlot);

                                    XYChart.Data cashPositionPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[0]));
                                    Rectangle rectangle1 = new Rectangle(0, 0);
                                    rectangle1.setVisible(false);
                                    cashPositionPlot.setNode(rectangle1);
                                    cashPositionSeries.getData().add(cashPositionPlot);

                                    XYChart.Data cashPositionMapPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[0]));
                                    Rectangle rectangle2 = new Rectangle(0, 0);
                                    rectangle2.setVisible(false);
                                    cashPositionMapPlot.setNode(rectangle2);
                                    cashPositionMapSeries.getData().add(cashPositionMapPlot);
                                }
                            }
                            savedP2PositionSeries = positionSeries;
                            savedP2CashPositionSeries = cashPositionSeries;
                            seriesList.add(positionSeries);
                            seriesList.add(positionMapSeries);
                            seriesList.add(cashPositionSeries);
                            seriesList.add(cashPositionMapSeries);
                            return seriesList;
                        }
                    };
                }
            };

            p2SeriesPopulator.stateProperty().addListener((v, oldState, newState) -> {
                switch (newState) {
                    case SCHEDULED:
                        System.out.println("scheduled");
                        break;
                    case READY:
                        System.out.println("ready");
                    case RUNNING:
                        break;
                    case SUCCEEDED:
                        p2Indicator.visibleProperty().unbind();
                        p2Indicator.setVisible(false);
                        p2Position.getData().clear();
                        p2CashPosition.getData().clear();
                        p2PositionMap.getData().clear();
                        p2CashPositionMap.getData().clear();
                        ArrayList<XYChart.Series> series = p2SeriesPopulator.valueProperty().getValue();
                        p2Position.getData().add(series.get(0));
                        p2PositionMap.getData().add(series.get(1));
                        p2CashPosition.getData().add(series.get(2));
                        p2CashPositionMap.getData().add(series.get(3));
                        p2EndCashPositionLbl.setText(p2EndCashPosition);
                        p2EndPositionLbl.setText(p2EndPosition);
                        p2EquityLbl.setText(p2Equity);
                        break;
                    case CANCELLED:
                        break;
                    case FAILED:
                        break;
                }
            });

            Service<BorderPane> p2SelectionPopulator =  new Service<BorderPane>() {
                @Override protected Task<BorderPane> createTask() {
                    return new Task<BorderPane>() {
                        @Override protected BorderPane call() throws Exception {
                            p2Selection = new Rectangle();
                            p2Selection.setFill(Color.web("blue", 0.1));
                            p2Selection.setStroke(Color.BLUE);
                            p2Selection.setStrokeDashOffset(50);

                            p2Selection.widthProperty().bind(p2SelectionCurrX.subtract(p2SelectionInitX));
                            p2Selection.heightProperty().setValue(55);
                            p2Selection.setVisible(false);

                            BorderPane p2SelectionPane = new BorderPane();

                            p2SelectionPane.setOnMouseClicked(p2SelectionHandler);
                            p2SelectionPane.setOnMouseDragged(p2SelectionHandler);
                            p2SelectionPane.setOnMouseEntered(p2SelectionHandler);
                            p2SelectionPane.setOnMouseExited(p2SelectionHandler);
                            p2SelectionPane.setOnMouseMoved(p2SelectionHandler);
                            p2SelectionPane.setOnMousePressed(p2SelectionHandler);
                            p2SelectionPane.setOnMouseReleased(p2SelectionHandler);

                            p2SelectionPane.getChildren().add(p2Selection);
                            return p2SelectionPane;
                        }
                    };
                }
            };

            p2SelectionPopulator.stateProperty().addListener((v, oldState, newState) -> {
                switch (newState) {
                    case SCHEDULED:
                        System.out.println("scheduled");
                        break;
                    case READY:
                        System.out.println("ready");
                    case RUNNING:
                        break;
                    case SUCCEEDED:
                        BorderPane selectionPane = p2SelectionPopulator.valueProperty().getValue();
                        p2Nav.getChildren().add(selectionPane);
                        break;
                    case CANCELLED:
                        break;
                    case FAILED:
                        break;
                }
            });

            p2Indicator.visibleProperty().bind(p2SeriesPopulator.progressProperty().isNotEqualTo(new SimpleDoubleProperty(ProgressBar.INDETERMINATE_PROGRESS)));
            p2SeriesPopulator.restart();
            p2SelectionPopulator.restart();

        } else {
            AlertBox.display("Missing Field", "Initial investment field is required");
        }
    }

    /**
     * Creates the portfolio for a given strategy, company and initial investment
     * Third portfolio
     * @throws IOException
     * @throws InterruptedException
     */
    public void p3RunBtnClicked() throws IOException, InterruptedException {
        if(!p3Initial.getText().isEmpty()){

            ProcessBuilder pb = new ProcessBuilder("python", "profiler.py",
                                                    p3SelectedStrategy,
                                                    p3Initial.getText(),
                                                    p3SelectedCompany);
            pb.redirectErrorStream(true);
            Process process = pb.start();
            process.waitFor();

            InputStream is = process.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);

            String p3FileName = "";
            String line;
            while ((line = br.readLine()) != null) {
                p3FileName = line;
            }

            p3Position.getXAxis().setAnimated(false);
            p3Position.getStylesheets().addAll(getClass().getResource("barCharts.css").toExternalForm());
            p3CashPosition.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());
            p3PositionMap.getStylesheets().addAll(getClass().getResource("mapBarCharts.css").toExternalForm());
            p3CashPositionMap.getStylesheets().addAll(getClass().getResource("lineCharts.css").toExternalForm());

            //service to create series (4 total)
            final String finalP3FileName = p3FileName;
            final Service<ArrayList<XYChart.Series>> p3SeriesPopulator = new Service<ArrayList<XYChart.Series>>() {
                @Override protected Task<ArrayList<XYChart.Series>> createTask() {
                    return new Task<ArrayList<XYChart.Series>>() {
                        @Override protected ArrayList<XYChart.Series> call() throws Exception {
                            updateProgress(0, 10);
                            ArrayList<XYChart.Series> seriesList = new ArrayList<>();
                            BufferedReader reader = new BufferedReader(new FileReader(finalP3FileName));
                            String currLine;
                            XYChart.Series positionSeries = new XYChart.Series();
                            XYChart.Series positionMapSeries = new XYChart.Series();
                            XYChart.Series cashPositionSeries = new XYChart.Series();
                            XYChart.Series cashPositionMapSeries = new XYChart.Series();
                            while((currLine = reader.readLine()) != null){
                                currLine = currLine.replaceAll("'", "");
                                if(currLine.contains("[")){
                                    currLine = currLine.replace("[", "");
                                    currLine = currLine.replace("]", "");
                                    String[] fields = currLine.split(",");
                                    p3EndCashPosition = fields[0];
                                    p3EndPosition = fields[1];
                                    p3Equity = fields[2];
                                } else {
                                    String[] fields = currLine.split(",");

                                    XYChart.Data positionPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[1]));
                                    positionSeries.getData().add(positionPlot);

                                    XYChart.Data positionMapPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[1]));
                                    positionMapSeries.getData().add(positionMapPlot);

                                    XYChart.Data cashPositionPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[0]));
                                    Rectangle rectangle1 = new Rectangle(0, 0);
                                    rectangle1.setVisible(false);
                                    cashPositionPlot.setNode(rectangle1);
                                    cashPositionSeries.getData().add(cashPositionPlot);

                                    XYChart.Data cashPositionMapPlot = new XYChart.Data(fields[2], Double.parseDouble(fields[0]));
                                    Rectangle rectangle2 = new Rectangle(0, 0);
                                    rectangle2.setVisible(false);
                                    cashPositionMapPlot.setNode(rectangle2);
                                    cashPositionMapSeries.getData().add(cashPositionMapPlot);
                                }
                            }
                            savedP3PositionSeries = positionSeries;
                            savedP3CashPositionSeries = cashPositionSeries;
                            seriesList.add(positionSeries);
                            seriesList.add(positionMapSeries);
                            seriesList.add(cashPositionSeries);
                            seriesList.add(cashPositionMapSeries);
                            return seriesList;
                        }
                    };
                }
            };

            p3SeriesPopulator.stateProperty().addListener((v, oldState, newState) -> {
                switch (newState) {
                    case SCHEDULED:
                        System.out.println("scheduled");
                        break;
                    case READY:
                        System.out.println("ready");
                    case RUNNING:
                        break;
                    case SUCCEEDED:
                        p3Indicator.visibleProperty().unbind();
                        p3Indicator.setVisible(false);
                        p3Position.getData().clear();
                        p3CashPosition.getData().clear();
                        p3PositionMap.getData().clear();
                        p3CashPositionMap.getData().clear();
                        ArrayList<XYChart.Series> series = p3SeriesPopulator.valueProperty().getValue();
                        p3Position.getData().add(series.get(0));
                        p3PositionMap.getData().add(series.get(1));
                        p3CashPosition.getData().add(series.get(2));
                        p3CashPositionMap.getData().add(series.get(3));
                        p3EndCashPositionLbl.setText(p3EndCashPosition);
                        p3EndPositionLbl.setText(p3EndPosition);
                        p3EquityLbl.setText(p3Equity);
                        break;
                    case CANCELLED:
                        break;
                    case FAILED:
                        break;
                }
            });

            Service<BorderPane> p3SelectionPopulator =  new Service<BorderPane>() {
                @Override protected Task<BorderPane> createTask() {
                    return new Task<BorderPane>() {
                        @Override protected BorderPane call() throws Exception {
                            p3Selection = new Rectangle();
                            p3Selection.setFill(Color.web("blue", 0.1));
                            p3Selection.setStroke(Color.BLUE);
                            p3Selection.setStrokeDashOffset(50);

                            p3Selection.widthProperty().bind(p3SelectionCurrX.subtract(p3SelectionInitX));
                            p3Selection.heightProperty().setValue(55);
                            p3Selection.setVisible(false);

                            BorderPane p3SelectionPane = new BorderPane();

                            p3SelectionPane.setOnMouseClicked(p3SelectionHandler);
                            p3SelectionPane.setOnMouseDragged(p3SelectionHandler);
                            p3SelectionPane.setOnMouseEntered(p3SelectionHandler);
                            p3SelectionPane.setOnMouseExited(p3SelectionHandler);
                            p3SelectionPane.setOnMouseMoved(p3SelectionHandler);
                            p3SelectionPane.setOnMousePressed(p3SelectionHandler);
                            p3SelectionPane.setOnMouseReleased(p3SelectionHandler);

                            p3SelectionPane.getChildren().add(p3Selection);
                            return p3SelectionPane;
                        }
                    };
                }
            };

            p3SelectionPopulator.stateProperty().addListener((v, oldState, newState) -> {
                switch (newState) {
                    case SCHEDULED:
                        System.out.println("scheduled");
                        break;
                    case READY:
                        System.out.println("ready");
                    case RUNNING:
                        break;
                    case SUCCEEDED:
                        BorderPane selectionPane = p3SelectionPopulator.valueProperty().getValue();
                        p3Nav.getChildren().add(selectionPane);
                        break;
                    case CANCELLED:
                        break;
                    case FAILED:
                        break;
                }
            });

            p3Indicator.visibleProperty().bind(p3SeriesPopulator.progressProperty().isNotEqualTo(new SimpleDoubleProperty(ProgressBar.INDETERMINATE_PROGRESS)));
            p3SeriesPopulator.restart();
            p3SelectionPopulator.restart();

        } else {
            AlertBox.display("Missing Field", "Initial investment field is required");
        }
    }

    /**
     * Generates the excel report
     * @throws IOException
     * @throws InterruptedException
     */
    public void genReportClicked() throws IOException, InterruptedException {
        PrintWriter writer = new PrintWriter("interfaceParams.txt");
        writer.println("True");
        for(String file : orders) {
            writer.println(file);
        }
        writer.close();

        //Call python module
        ProcessBuilder pb = new ProcessBuilder("python", "javaToPyInterface.py");
        pb.redirectErrorStream(true);
        Process process = pb.start();
        //Pause thread until interface is done
        process.waitFor();

        InputStream is = process.getInputStream();
        InputStreamReader isr = new InputStreamReader(is);
        BufferedReader br = new BufferedReader(isr);

        String reportName = "";

        String line;
        while ((line = br.readLine()) != null) {
            reportName = line;
        }

        boolean openReport = ConfirmBox.display("Report Generated", "The report has been generated. Open now?");
        if(openReport){
            ProcessBuilder pb2 = new ProcessBuilder("open", reportName);
            Process process2 = pb2.start();
            process2.waitFor();
        }
    }

    /**
     * Generates the csv dump
     * @throws IOException
     * @throws InterruptedException
     */
    public void genCSVClicked() throws IOException, InterruptedException {
        PrintWriter writer = new PrintWriter("interfaceParams.txt");
        writer.println("csvDump");
        for(String file : orders) {
            writer.println(file);
        }
        writer.close();

        ProcessBuilder pb = new ProcessBuilder("python", "javaToPyInterface.py");
        pb.redirectErrorStream(true);
        Process process = pb.start();
        //Pause thread until interface is done
        process.waitFor();

        InputStream is = process.getInputStream();
        InputStreamReader isr = new InputStreamReader(is);
        BufferedReader br = new BufferedReader(isr);

        String csvName = "";

        String line;
        while ((line = br.readLine()) != null) {
            csvName = line;
        }

        boolean answer = ConfirmBox.display("Report Generated", "The csv has been made: " + csvName);
        if(answer){
            ProcessBuilder pb2 = new ProcessBuilder("open", ".");
            Process process2 = pb2.start();
            process2.waitFor();
        }
    }

    /**
     * Input sanitation
     * @return True if input is okay to use, False otherwise
     */
    public boolean handleData() throws FileNotFoundException {

        //Pull data file
        String dataString = dataPath.getText();
        if (dataFile != null) dataString = dataFile;

        //Pull start and end dates
        String startString = startInput.getText();
        String endString = endInput.getText();

        //Pull the selected strategies
        String strategyString = strategy1.getValue();
        if (!strategy2.getValue().equals("(optional)")) {
            strategyString = strategyString + ", " + strategy2.getValue();
        }

        //Pull from the input fields + file chooser
        //Strategy 1
        String nString1 = nInput1.getText();
        String thString1 = thInput1.getText();
        //Strategy 2
        String nString2 = nInput2.getText();
        String thString2 = thInput2.getText();

        //Remove whitespace
        strategyString = strategyString.replaceAll("\\s+", "");
        nString1 = nString1.replaceAll("\\s+", "");
        thString1 = thString1.replaceAll("\\s+", "");
        nString2 = nString2.replaceAll("\\s+", "");
        thString2 = thString2.replaceAll("\\s+", "");

        //Separate by commas
        List<String> stratList = Arrays.asList(strategyString.split(","));
        //Strategy1
        List<String> nList1 = Arrays.asList(nString1.split(","));
        List<String> thList1 = Arrays.asList(thString1.split(","));
        //Strategy2
        List<String> nList2 = Arrays.asList(nString2.split(","));
        List<String> thList2 = Arrays.asList(thString2.split(","));

        //If no data file was selected
        if (dataString.equals("No file selected.")){
            AlertBox.display("Invalid Input", "No file selected.");
            return false;
        }

        //If number of n params doesn't match number of threshold params
        if ((nList1.size() != thList1.size()) && (nList2.size() != thList2.size())) {
            AlertBox.display("Invalid Input", "Number of N parameters does not match number of threshold parameters");
            return false;
        }

        //If missing date input
        if(startString.isEmpty() || endString.isEmpty()){
            AlertBox.display("Missing Year", "Start Year and/or End Year field is missing");
            return false;
        }

        //If strategy 1 is missing parameters
        if(!stratList.get(0).equals("WilliamsR")) {     //If strategy 1 is not WilliamsR
            if (nString1.isEmpty() || thString1.isEmpty()) {
                AlertBox.display("Missing Input", "One or more required fields missing in Strategy 1");
                return false;
            }
        } else {                                        //If strategy 1 is WilliamsR
            if (nString1.isEmpty()){
                AlertBox.display("Missing Input", "Missing N value(s) in Strategy 1");
                return false;
            }
        }

        //If strategy 2 is missing parameters (given strategy 2 is selected)
        if(stratList.size() == 2) {
            if(!stratList.get(1).equals("WilliamsR")) {  //If strategy 1 is not WilliamsR
                if (nString2.isEmpty() || thString2.isEmpty()) {
                    AlertBox.display("Missing Input", "One or more required fields missing in Strategy 2");
                    return false;
                }
            } else {                                    //If strategy 1 is WilliamsR
                if(nString2.isEmpty()){
                    AlertBox.display("Missing Input", "Missing N value(s) in Strategy 2");
                    return false;
                }
            }
        }


        //Write params to a file
        PrintWriter writer = new PrintWriter("interfaceParams.txt");
        writer.println("False");
        //Strategy 1
        for (int i = 0; i < nList1.size(); i++) {
            writer.println(stratList.get(0));
            writer.println(nList1.get(i));
            if(!stratList.get(0).equals("WilliamsR")) {
                writer.println(thList1.get(i));
            } else {
                writer.println("---");
            }
            writer.println(startString);
            writer.println(endString);
            writer.println(dataString);
        }

        //Strategy 2
        if(stratList.size() == 2){
            for (int i = 0; i < nList2.size(); i++) {
                writer.println(stratList.get(1));
                writer.println(nList2.get(i));
                if(!stratList.get(1).equals("WilliamsR")) {
                    writer.println(thList2.get(i));
                } else {
                    writer.println("---");
                }
                writer.println(startString);
                writer.println(endString);
                writer.println(dataString);
            }
        }

        writer.close();

        return true;

    }

}
