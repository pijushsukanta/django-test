import math
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
      # Set the number of items you want per page
    page_size_query_param = 'page_size'
    max_page_size = 100
    
def get_paginated(page_size,queryset,request):
    
    paginator = CustomPagination()
    paginator.page_size = page_size
    paginated_queryset = paginator.paginate_queryset(queryset,request)
    
    return paginator.get_paginated_response(paginated_queryset).data
  
  
def get_paginated_data(page, total_page, data, per_page=100):
        print(per_page)
        if data == [] or len(data) == 0:
            print(per_page)
            return  {
            "current_page": 0,
            "next_page": 0,
            "prev_page": 0,
            "has_prev": 0,
            "has_next": 0,
            "total_page": 1,
            "data": []
        } 
        
        page_num = total_page
        
        print(page_num)
        page_num = math.ceil(page_num / per_page)
        print(page_num)

        next_page = page + 1
        prev_page = (page - 1) if (page - 1) > 1 else page
        has_prev = True
        has_next = True
        if page == 1:
            prev_page = 1
            has_prev = False
        if page >= page_num:
            has_next = False


        page_data = {
            "current_page": page,
            "next_page": next_page,
            "prev_page": prev_page,
            "has_prev": has_prev,
            "has_next": has_next,
            "total_page": page_num,
            "data": data
        }
        
        print(page_data)

        return page_data