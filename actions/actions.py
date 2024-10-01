from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

  # Các mảng chứa các địa điểm
chonoicairang_arr = ["chợ nổi cái răng cần thơ", "chợ nổi cái răng", "chợ nổi", "cho noi cai rang", "cho noi", "cai rang"]
benninhkieu_arr = ["bến ninh kiều", "ninh kiều", "ben ninh kieu", "ninh kieu", "ben", "benninhkieu"]
langmykhanh_arr = ["làng du lịch mỹ khánh", "du lịch mỹ khánh", "làng du lịch", "mỹ khánh", "lang my khanh", "lang du lich","làng mỹ khánh"]
thienvientruc_arr = ["thiền viện trúc lâm phương nam", "thiền viện trúc lâm", "thiền viện", "thiền viện phương nam", "thien vien truc lam phuong nam", "thien vien truc", "thien vien", "thien vien truc lam", "truc lam phuong nam"]
vuoncobanglang_arr = ["vườn cò bằng lăng", "vườn cò", "vuon co","vườn", "vườn cò bằng", "vuon co bang lang"]
restaurant_arr=["nha hang","nhà hàng buffet","buffet","quan an","quán ăn vặt","quán cà phê","món chay","cho an uong","chỗ ăn","mon an","dac san","cho an","restaurant","hủ tiếu ngon","món đặc trưng miền Tây","quán ăn hải sản","nhà hàng trên sông","quán ăn","nhà hàng","món ăn","món chay","địa điểm ăn uống","món ăn nổi bật","mon chay","mon an ngon","quán bún","quán cơm","cơm"]
hotel_arr= ["nhà nghỉ","khách sạn","chỗ nghỉ","chỗ ở","phòng trọ","chỗ nghỉ chân","khu nghỉ dưỡng","cho nghi ngoi","cho ngu","khach san","nha nghi","hotel"]
vehicle_arr=["phương tiện","thuê xe nào","đi thuyền","xe ôm","xe buýt","taxi","xe máy","đi bộ","dịch vụ cho thuê xe","phương tiện nào là tốt nhất","xe bus"]
 
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Gửi thông điệp khi chatbot không hiểu
        response = "Xin lỗi, tôi không hiểu yêu cầu của bạn. Bạn có thể nói rõ hơn không?"
        
        # Gửi phản hồi đến người dùng
        dispatcher.utter_message(text=response)
        
        return []
    
class ActionExtractLocation(Action):
    def name(self) -> Text:
        return "action_extract_location"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Trích xuất và chuẩn hóa giá trị thực thể
        location_entity = next(tracker.get_latest_entity_values("location"), None)
        restaurant_entity = next(tracker.get_latest_entity_values("restaurant"), None)
        hotel_entity = next(tracker.get_latest_entity_values("hotel"), None)
        vehicle_entity = next(tracker.get_latest_entity_values("vehicle"), None)
        budget_entity = next(tracker.get_latest_entity_values("budget"), None)
        
        if location_entity:
            location_entity = location_entity.lower()
        
        # Kiểm tra xem có thực thể nào khác ngoài location
        other_entities = {
            "restaurant": restaurant_entity.lower() if restaurant_entity else None,
            "vehicle": vehicle_entity.lower() if vehicle_entity else None,
            "hotel": hotel_entity.lower() if hotel_entity else None,
            "budget": budget_entity.lower() if budget_entity else None
        }
        print(budget_entity, " " ,location_entity)
        # Địa điểm du lịch và các dịch vụ tương ứng
        location_services = {
            "chonoicairang_arr": "utter_ask_chonoicairang",
            "benninhkieu_arr": "utter_ask_benninhkieu",
            "langmykhanh_arr": "utter_ask_langmykhanh",
            "thienvientruc_arr": "utter_ask_thienvientruc",
            "vuoncobanglang_arr": "utter_ask_vuoncobanglan"
        }
        
        if budget_entity == None: 
            # Kiểm tra các địa điểm
            for location_arr, response in location_services.items():
                # Kiểm tra xem location_entity có thuộc vào các địa điểm trong danh sách không
                if location_entity in globals().get(location_arr, []):
                    print(f"Địa điểm tìm thấy: {location_entity} trong {location_arr}")

                    # Kiểm tra các dịch vụ khác (nếu có)
                    for entity_type, entity_value in other_entities.items():
                        print("entity", entity_type)
                        if entity_value:
                            service_response = f"utter_ask_{entity_type}_{location_arr[:-4]}"
                            dispatcher.utter_message(response=service_response)
                            return []
                    
                    # Nếu không có dịch vụ cụ thể nào được hỏi
                    dispatcher.utter_message(response=response)
                    return []
        else :
            donViNghin= ['k','nghìn','ngìn','nghin','ngin']
            donViTrieu = ['tr','trieu','triệu','củ']
            donVikhac = ['giá rẻ','gia re','rẻ','thấp','giá thấp']
            parts = budget_entity.split() 
            so = 0
            
            # Phân tích ngân sách
            parts = budget_entity.split()
            numbers = ''.join([char for char in budget_entity if char.isdigit()])
            if numbers:
                if len(parts) == 2:
                    so = int(parts[0])
                    donVi = parts[1]
                    if donVi in donViNghin:
                        so *= 1000
                    elif donVi in donViTrieu:
                        so *= 1000000
                else:
                    so = int(numbers)
                    donVi = budget_entity.replace(str(so), '')
                    if donVi in donViNghin:
                        so *= 1000
                    elif donVi in donViTrieu:
                        so *= 1000000
            
            # Kiểm tra địa điểm và phản hồi theo ngân sách
            for location_arr, response in location_services.items():
                if location_entity in globals().get(location_arr, []):
                    if so <= 1500000 or budget_entity in donVikhac:
                        dispatcher.utter_message(response=f"utter_{location_arr[:-4]}_hotel_duoi_1trieu")  
                    elif so < 3000000:
                        dispatcher.utter_message(response=f"utter_{location_arr[:-4]}_hotel_duoi_3trieu")
                    else:
                        dispatcher.utter_message(response=f"utter_{location_arr[:-4]}_hotel_tren_3trieu") 
                    return []  # Dừng sau khi đã phản hồi

        # Nếu không tìm thấy địa điểm
        dispatcher.utter_message(text="Hãy nói rõ tên địa điểm bạn quan tâm và loại hình dịch vụ như khách sạn, quán ăn, phương tiện.")
        return []

