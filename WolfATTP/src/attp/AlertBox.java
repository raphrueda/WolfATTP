package attp;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.stage.Modality;
import javafx.stage.Stage;


/**
 * Created by Raphael on 10/05/2015.
 */
public class AlertBox {
    public static void display(String title, String msg){
        Stage window = new Stage();
        window.initModality(Modality.APPLICATION_MODAL);
        window.initModality(Modality.NONE);
        window.setTitle(title);
        window.setMinWidth(250);
        window.setResizable(false);

        Label label = new Label(msg);
        Button close = new Button("Close");
        close.setOnAction(event -> window.close());

        VBox layout = new VBox(10);
        layout.getChildren().addAll(label, close);
        layout.setAlignment(Pos.CENTER);

        layout.setPadding(new Insets(20,20,10,20));

        Scene scene = new Scene(layout);
        window.setScene(scene);
        window.showAndWait();
    }
}
