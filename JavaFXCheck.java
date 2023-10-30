public class JavaFXCheck {
    public static void main(String[] args) {
        try {
            Class.forName("javafx.application.Application");
            System.out.println("JavaFX is available on your system.");
        } catch (ClassNotFoundException e) {
            System.out.println("JavaFX is not available on your system.");
        }
    }
}
