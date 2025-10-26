from rest_framework.response import Response

class CustomResponse(Response):
    """
    A custom response class for Django REST Framework that adds a `status_code`
    attribute to the response data.
    """
    def __init__(self, data=None, status=None,message = None, **kwargs):
        data = {'status_code': status, 'data': data,'messages' : message}
        super().__init__(data=data,status=status, **kwargs)

class CustomMessage():

    def __init__(self,type = None,data = None) :
        self.message = None
        if(type == 1):
             self.message = self.ok()
        elif(type == 2):
             self.message = self.error(data)
        elif(type == 3):
             self.message = self.required(data)
        elif( type == 4):
             self.message = self.not_found(data)
        elif(type == 5):
             self.message = self.add(data)
        elif(type == 6):
             self.message = self.edit(data)
        elif(type == 7):
             self.message = self.delete(data)
        else:
            self.message = data
        
    
        

    def ok(self):
        return "درخواست موفقیت آمیز است"

    def error(self,message):

        return message +" با خطا مواجه شد " 

    def required(self,fields):
        if type(fields) == str:
            return fields
        ans= ""
        for key in fields:
            ans += str(fields[key][0]) + " "
        return ans
    
    def not_found(self,data):
        return data + "  مورد نظر یافت نشد "
    def add(self,data) :
        return data + " با موفقیت افزوده شد "
    
    def delete(self,data) :
        return data + " با موفقیت حذف شد "
    
    def edit(self,data) :
        return data + " با موفقیت ویرایش شد "
    
    
def message_generator (field_fa,type):
    if(type == 1):
        return field_fa +" اجباری است "
    
   