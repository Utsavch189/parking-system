from .auth_admin_service import login,register
from .parking_area_service import create_parking_area,update_parking_area,get_all_parking_areas,parkingarea_delete_confirmation_mail,parkingarea_actual_delete
from .parking_attendants_service import get_all_attendants,attendant_delete_confirmation_mail,attendant_actual_delete,attendant_verify_toggle,attendant_suspend_toggle