import java.io.*;
import java.util.*;
import java.lang.RuntimeException;

public class ReportBugFixes {

    public HashMap<String, String> parseCSV(final String csvFile) {
        HashMap<String, String> map = new HashMap<>();
        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            String line;
            line = br.readLine(); // Ignore the first line as it contains the header and not data.
            while ((line = br.readLine()) != null) {

                // use comma as separator
                String[] tokens = line.split(",");
                if (tokens.length < 2)
                    throw new RuntimeException("Wrongly formatted csv file!!");
                String[] tokenizeLink = tokens[0].split("/");
                if (tokenizeLink.length < 2)
                    throw new RuntimeException("Wrongly formatted link " + tokens[0]);
                String repoName = tokenizeLink[tokenizeLink.length-2]+ "/" + tokenizeLink[tokenizeLink.length-1];
                map.put(repoName, tokens[1]);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return map;
    }

    public static void main(String[] args) {
        ReportBugFixes report = new ReportBugFixes();
        HashMap<String, String> map = report.parseCSV("resources/projects.csv");
        for(String key: map.keySet()){
            System.out.println(key + " " + map.get(key));
        }
    }
}
