import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import org.apache.nifi.processor.io.StreamCallback

// Define a shared object to hold "global" variables
class GlobalState {
    static boolean errorOccurred = false
}

class GetEveryPage implements StreamCallback {
    @Override
    void process(InputStream inputStream, OutputStream outputStream) {
        try {
            def inputText = inputStream.text
            def asjson = new JsonSlurper().parseText(inputText)

            def pagination = asjson?.metadata?.pagination
            if (pagination?.page && pagination.page <= pagination.pages) {
                def url = pagination.next_page_url
                def connection = new URL(url).openConnection()
                def rawReply = connection.inputStream.text

                def reply = new JsonSlurper().parseText(rawReply)
                outputStream.write(JsonOutput.prettyPrint(JsonOutput.toJson(reply)).bytes)
            } else {
                global errorOccurred
                GlobalState.errorOccurred = true
                // log.info("Last page reached or pagination metadata missing.")
                outputStream.write(JsonOutput.prettyPrint(JsonOutput.toJson(asjson)).bytes)
            }
        } catch (Exception e) {
            GlobalState.errorOccurred = true
            throw new RuntimeException("Error fetching pages: " + e.message, e)
        }
    }
}

GlobalState.errorOccurred = false
def flowFile = session.get()
if (flowFile != null) {
    try {
        flowFile = session.write(flowFile, new GetEveryPage())
        if (GlobalState.errorOccurred) {
            session.transfer(flowFile, REL_FAILURE)
        } else {
            session.transfer(flowFile, REL_SUCCESS)
        }
    } catch (Exception e) {
        GlobalState.errorOccurred = true
        // log.error("Error processing FlowFile: ${e.message}", e)
        session.transfer(flowFile, REL_FAILURE)
    }
}