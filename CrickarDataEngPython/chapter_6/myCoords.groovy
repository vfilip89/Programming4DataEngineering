import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import org.apache.nifi.processor.io.StreamCallback

class MyCoords implements StreamCallback {
    @Override
    void process(InputStream inputStream, OutputStream outputStream) {
        try {
            def inputText = inputStream.text
            def reply = new JsonSlurper().parseText(inputText)

            // Adding 'coords' field
            reply['coords'] = "${reply.lat},${reply.lng}"

            // Adding 'opendate' field
            def dateParts = reply.created_at?.split('T')
            reply['opendate'] = dateParts ? dateParts[0] : null

            outputStream.write(JsonOutput.prettyPrint(JsonOutput.toJson(reply)).bytes)
        } catch (Exception e) {
            throw new RuntimeException("Error processing JSON: " + e.message, e)
        }
    }
}

def flowFile = session.get()
if (flowFile != null) {
    try {
        flowFile = session.write(flowFile, new MyCoords())
        session.transfer(flowFile, REL_SUCCESS)
    } catch (Exception e) {
        log.error("Error processing FlowFile: ${e.message}", e)
        session.transfer(flowFile, REL_FAILURE)
    }
}