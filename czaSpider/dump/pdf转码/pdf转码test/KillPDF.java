import java.io.File;
import java.io.IOException;

public class KillPDF {

    public static void main(String[] args) {
        String batPath = "C:/Users/czaOrz/Desktop/kill_pdf_process.bat";
        File batFile = new File(batPath);
        boolean batFileExist = batFile.exists();
        System.out.println("batFileExist:" + batFileExist);
        if (batFileExist) {
            callCmd(batPath);
        }
    }

    private static void  callCmd(String locationCmd){

        StringBuilder sb = new StringBuilder();
        try {
            Process child = Runtime.getRuntime().exec(locationCmd);
            System.out.println("callCmd execute finished");
        } catch (IOException e) {
            System.out.println(e);
        }
    }
}