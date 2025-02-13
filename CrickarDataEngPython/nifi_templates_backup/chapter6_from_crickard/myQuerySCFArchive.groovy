import org.apache.nifi.processor.io.StreamCallback
import org.apache.commons.io.IOUtils
import java.nio.charset.StandardCharsets
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

// Custom StreamCallback implementation
class ModJSON implements StreamCallback {
    @Override
    void process(InputStream inputStream, OutputStream outputStream) {
        def errorOccurred = false
        try {
            // Construct the API URL with parameters
            def placeUrl = "bernalillo-county"
            def perPage = 100
            def status = "Archived"
            def apiUrl = "https://seeclickfix.com/api/v2/issues?place_url=${placeUrl}&per_page=${perPage}&status=${status}"

            // Make HTTP request and parse JSON response
            def connection = new URL(apiUrl).openConnection()
            connection.setRequestMethod("GET")
            connection.setRequestProperty("Accept", "application/json")
            connection.connect()

            def rawReply = connection.inputStream.text
            def jsonReply = new JsonSlurper().parseText(rawReply)

            // Write the JSON response to the output stream
            outputStream.write(JsonOutput.prettyPrint(JsonOutput.toJson(jsonReply)).getBytes(StandardCharsets.UTF_8))
        } catch (Exception e) {
            errorOccurred = true
            log.error("Error occurred while fetching data from API: ${e.message}", e)

            // Handle the error by writing a failure response
            def errorResponse = [error: "An error occurred during the script execution"]
            outputStream.write(JsonOutput.prettyPrint(JsonOutput.toJson(errorResponse)).getBytes(StandardCharsets.UTF_8))
        }
    }
}

// Main script logic
def flowFile = session.get()
if (flowFile != null) {
    try {
        flowFile = session.write(flowFile, new ModJSON())
        session.transfer(flowFile, REL_SUCCESS)
    } catch (Exception e) {
        log.error("Error processing FlowFile: ${e.message}", e)
        session.transfer(flowFile, REL_FAILURE)
    }
}