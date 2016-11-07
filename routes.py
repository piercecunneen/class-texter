import Get_messages
import Get_Sorted_CRNs
import dbfunction
import time

def create_class_opening_instance(crn = "20065", num = "6109522515" ):
		sorted_crn_numbers = Get_Sorted_CRNs.Get_CRN_List()
		subject = Get_Sorted_CRNs.is_Valid(int(crn), sorted_crn_numbers)
		if subject:
			dbfunction.add_row({'phone_number': num, 'crn':crn}, subject)
			Message = Get_messages.Send_Reply_Inquiry(num)
			if Message:
				return 1
		return 0





crn = "20065"
num = "6109522515"
sorted_crn_numbers = Get_Sorted_CRNs.Get_CRN_List()
# subject = Get_Sorted_CRNs.is_Valid(int(crn), sorted_crn_numbers)
# dbfunction.add_row({'phone_number': num, 'crn':crn}, subject)
# Get_messages.Send_Reply_Inquiry(num)
# time.sleep(15)
# Get_messages.Check_For_Responses()
# dbfunction.verify_number(num)
Get_messages.Check_for_openings()
