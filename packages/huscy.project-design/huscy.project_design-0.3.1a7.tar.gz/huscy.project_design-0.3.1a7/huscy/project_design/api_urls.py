from rest_framework_nested.routers import NestedDefaultRouter

from huscy.project_design import views
from huscy.projects.urls import project_router


project_router.register('experiments', views.ExperimentViewSet, basename='experiment')

experiment_router = NestedDefaultRouter(project_router, 'experiments', lookup='experiment')
experiment_router.register('sessions', views.SessionViewSet, basename='session')

session_router = NestedDefaultRouter(experiment_router, 'sessions', lookup='session')
session_router.register('dataacquisitionmethods', views.DataAcquisitionMethodViewSet,
                        basename='dataacquisitionmethod')

urlpatterns = []
urlpatterns += project_router.urls
urlpatterns += experiment_router.urls
urlpatterns += session_router.urls
