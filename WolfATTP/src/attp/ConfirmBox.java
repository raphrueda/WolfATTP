package attp;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Modality;
import javafx.stage.Stage;


/**
 * Created by Raphael on 10/05/2015.
 */
public class ConfirmBox {

    static boolean answer;

    public static boolean display(String title, String msg){
        Stage window = new Stage();
        window.initModality(Modality.APPLICATION_MODAL);
        window.setTitle(title);
        window.setMinWidth(250);
        window.setResizable(false);
        Label label = new Label(msg);

        Button yesBtn = new Button("Yes");
        Button noBtn = new Button("No");

        yesBtn.setOnAction(event -> {
            answer = true;
            window.close();
        });
        noBtn.setOnAction(event -> {
            answer = false;
            window.close();
        });

        VBox layout = new VBox(10);
        HBox btns = new HBox();
        btns.setSpacing(10);
        btns.setAlignment(Pos.CENTER);
        btns.getChildren().addAll(yesBtn,noBtn);

        layout.getChildren().addAll(label, btns);
        layout.setAlignment(Pos.CENTER);
        layout.setPadding(new Insets(20, 20, 10, 20));
        Scene scene = new Scene(layout);
        window.setScene(scene);
        window.showAndWait();

        return answer;
    }
}
