from django.urls import path
from . import views
 
urlpatterns = [
    path('profile/', views.exam_committe_profile, name="exam_committe_profile"),
    path('exam_committte_current_courses/', views.exam_committte_current_courses, name="exam_committte_current_courses"),
    path('exam_committte_special_courses/', views.exam_committte_special_courses, name="exam_committte_special_courses"),
    path('exam_committe_course_details/<str:course_code>/', views.exam_committe_course_details, name="exam_committe_course_details"),
    path('exam_committe_logout/', views.exam_committe_logout, name="exam_committe_logout"),
    path('course_teacher_marks/<str:course_code>/', views.course_teacher_marks, name="course_teacher_marks"),
    path('external_teacher_marks/<str:course_code>/', views.external_teacher_marks, name="external_teacher_marks"),
    path('details_external_teacher_marks/<str:course_code>/', views.details_external_teacher_marks, name="details_external_teacher_marks"),
    path('edit_external_teacher_marks/<str:course_code>/', views.edit_external_teacher_marks, name="edit_external_teacher_marks"),
    path('compare_internal_external_marks/<str:course_code>/', views.compare_internal_external_marks, name="compare_internal_external_marks"),
    path('edit_third_examinner_mark/<str:course_code>/', views.edit_third_examinner_mark, name="edit_third_examinner_mark"),
    path('mark_sheet_details/<str:course_code>/', views.mark_sheet_details, name="mark_sheet_details"),
    path('show_all_marks/<str:course_code>/', views.show_all_marks, name="show_all_marks"),
    path('exam_committte_research_project/<str:course_code>/', views.exam_committte_research_project, name="exam_committte_research_project"),
    path('external_teacher_research_project_marks/<str:course_code>/', views.external_teacher_research_project_marks, name="external_teacher_research_project_marks"),
    path('show_external_research_project_marks/<str:course_code>/', views.show_external_research_project_marks, name="show_external_research_project_marks"),
    path('edit_external_research_project_marks/<str:course_code>/', views.edit_external_research_project_marks, name="edit_external_research_project_marks"),
    path('course_teacher_research_project_marks/<str:course_code>/', views.course_teacher_research_project_marks, name="course_teacher_research_project_marks"),
    path('check_third_examinner_research_project_marks/<str:course_code>/', views.check_third_examinner_research_project_marks, name="check_third_examinner_research_project_marks"),
    path('show_research_projects_all_marks/<str:course_code>/', views.show_research_projects_all_marks, name="show_research_projects_all_marks"),
    path('edit_third_examinner_research_project_mark/<str:course_code>/', views.edit_third_examinner_research_project_mark, name="edit_third_examinner_research_project_mark"),
    path('final_consoilated_research_project_marksheet/<str:course_code>/', views.final_consoilated_research_project_marksheet, name="final_consoilated_research_project_marksheet"),
    path('exam_committe_lab_course_details/<str:course_code>/', views.exam_committe_lab_course_details, name="exam_committe_lab_course_details"),
    path('exam_committe_viva_course_details/<str:course_code>/', views.exam_committe_viva_course_details, name="exam_committe_viva_course_details"),
    path('exam_committe_project_course_details/<str:course_code>/', views.exam_committe_project_course_details, name="exam_committe_project_course_details"),
    path('semester_final_result/<str:semester_no>/', views.semester_final_result, name="semester_final_result"),
]