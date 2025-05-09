from rest_framework.response import Response

class CustomResponse(Response):
    """
    A custom response class for Django REST Framework that adds a `status_code`
    attribute to the response data.
    """
    def __init__(self, data=None, status=None,message = None, **kwargs):
        data = {'status_code': status, 'data': data,'messages' : message.message}
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
    
   

def convert_form_to_list(form):
    new_form = {}
    main_keys = set()
    for key in form:
        if("]." in key):
            main_key = key.split("[")[0]
            main_keys.add(main_key)
            sub_key = key.split(".")[1]
            new_key = key.split("]")[0].split("[")[1]
            if(main_key not in new_form):
                new_form[main_key] = {}
            if(new_key not in new_form[main_key]):
                new_form[main_key][new_key] = []
            new_form[main_key][new_key].append({sub_key: form[key]})
        else:
            new_form[key] = form[key]
    for main_key in main_keys:
        main_array=[]
        for key in new_form[main_key]:
            temp_array=new_form[main_key][key]
            data={}
            for i in temp_array:
                for k in i:
                    data[k] = i[k]
            main_array.append(data)
        new_form[main_key] = main_array

    return new_form
        
