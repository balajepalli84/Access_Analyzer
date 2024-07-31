import oci
import datetime
# Initialize the OCI Config
config = oci.config.from_file()
audit = oci.audit.AuditClient(config)
# Create the Identity Client
identity_client = oci.identity.IdentityClient(config)
def list_audit_events(audit,compartment_id, start_time, end_time):
    events = []
    next_page = None
    while True:
        response = audit.list_events(
            compartment_id=compartment_id,
            start_time=start_time,
            end_time=end_time,
            page=next_page
        )
        events.extend(response.data)
        if not response.has_next_page:
            break
        next_page = response.next_page
    return events

c='ocid1.compartment.oc1..aaaaaaaafklcekq7wnwrt4zxeizcrmvhltz6wxaqzwksbhbs73yz6mtpi5za'
end_time = datetime.datetime.utcnow()
start_time = end_time + datetime.timedelta(days=-5)
list_events_response=list_audit_events(audit,c, start_time, end_time)
print(list_events_response)