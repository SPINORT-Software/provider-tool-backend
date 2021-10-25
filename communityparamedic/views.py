from .serializers import *
from rest_framework import status, generics, response, views
from rest_framework.response import Response


class WorkloadList(generics.ListCreateAPIView):
    """
    List all workload.
    """
    queryset = DailyWorkLoad.objects.all()
    serializer_class = DailyWorkloadSerializer


class WorkloadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Add a workload, update a workload detail, delete a workload
    """
    queryset = DailyWorkLoad.objects.all()
    serializer_class = DailyWorkloadSerializer


class AssessmentList(generics.ListCreateAPIView):
    """
    List all Client Assessment.
    """
    queryset = CommunityClientAssessment.objects.all()
    serializer_class = CommunityClientAssessmentSerializer


class AssessmentCreate(views.APIView):
    """
    Create an assessment record.
    """

    def join_list(self, list_items):
        if isinstance(list_items, list):
            return "$$$".join(list_items)
        return list_items

    def post(self, request, format=None):
        request_data = request.data
        client_status = request_data.get('client_status')

        if "assessment_type_data" in request_data:
            assessment_data = request_data["assessment_type_data"]

            if client_status == "NEW_CASE_MANAGEMENT_CLIENT":
                if "vital_signs" in assessment_data:
                    return self.newclient_assessment(assessment_data, request_data)
                else:
                    return Response("Missing vital signs data in the assessment.", status=status.HTTP_400_BAD_REQUEST)
            elif client_status == "EXISTING_CASE_MANAGEMENT_CLIENT":
                if all(key in assessment_data for key in
                       ("changes_in_condition", "vital_signs", "home_safety_assessment")):
                    return self.existingclient_assessment(assessment_data, request_data)
                else:
                    return Response("Missing required data values.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Invalid client status value provided.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid request.", status=status.HTTP_400_BAD_REQUEST)

    def newclient_assessment(self, assessment_data, request_data):
        vital_signs_serializer = ClientVitalSignsSerializer(data=assessment_data.get('vital_signs'))
        if vital_signs_serializer.is_valid():
            vital_signs_object = vital_signs_serializer.save()
            assessment_data["vital_signs"] = vital_signs_object.vital_signs_id

            """
            Process list type data fields into strings
            """
            assessment_data["priority_problems"] = self.join_list(assessment_data["priority_problems"])
            assessment_data["interventions"] = self.join_list(assessment_data["interventions"])
            assessment_data["recommendations"] = self.join_list(assessment_data["recommendations"])

            """
            Create New Client Assessment object
            """
            new_case_client_serializer = NewCaseClientAssessmentSerializer(data=assessment_data)
            if new_case_client_serializer.is_valid():
                new_case_client_object = new_case_client_serializer.save()

                # Add Home Safety Assessment
                self.add_home_safety(assessment_data, new_case_client_object)

                client_assessment_serializer = CommunityClientAssessmentSerializer(data={
                    "community_paramedic": request_data.get('community_paramedic'),
                    "client": request_data.get("client"),
                    "client_status": request_data.get("client_status"),
                    "new_case_client_assessment": new_case_client_object.assessment_id
                })

                if client_assessment_serializer.is_valid():
                    client_assessment_serializer.save()
                    return Response("Successfully added client assessment record.",
                                    status=status.HTTP_201_CREATED)
                else:
                    print(client_assessment_serializer.errors)
                    return Response("Failed to create client assessment record.",
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                print(new_case_client_serializer.errors)
                return Response("Invalid client assessment data provided.",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid vital signs data in the assessment.",
                            status=status.HTTP_400_BAD_REQUEST)

    def add_condition_changes(self, condition_changes_data):
        condition_changes_data["mental_status_changes"] = self.join_list(
            condition_changes_data["mental_status_changes"])
        condition_changes_data["functional_status_changes"] = self.join_list(
            condition_changes_data["functional_status_changes"])
        condition_changes_data["respiratory_changes"] = self.join_list(condition_changes_data["respiratory_changes"])
        condition_changes_data["gi_abdomen_changes"] = self.join_list(condition_changes_data["gi_abdomen_changes"])
        condition_changes_data["gu_urine_changes"] = self.join_list(condition_changes_data["gu_urine_changes"])

        condition_changes_serializer = ExistingCaseClientAssessmentChangeInConditionSerializer(
            data=condition_changes_data)
        if condition_changes_serializer.is_valid():
            condition_changes_object = condition_changes_serializer.save()
            return condition_changes_object.change_in_condition_id
        return False

    def add_home_safety(self, assessment_data, new_case_client_object):
        home_safety_assessment_data = assessment_data.get('home_safety_assessment', None)
        if home_safety_assessment_data:
            for hsa_item in home_safety_assessment_data.items():
                hsa_serializer = HomeSafetyAssessmentSerializer(data={
                    "question": hsa_item[0],
                    "answer": hsa_item[1],
                    "new_client_assessment": new_case_client_object.assessment_id
                })
                if hsa_serializer.is_valid():
                    hsa_serializer.save()

    def existingclient_assessment(self, assessment_data, request_data):
        vital_signs_serializer = ClientVitalSignsSerializer(data=assessment_data.get('vital_signs'))
        if vital_signs_serializer.is_valid():
            vital_signs_object = vital_signs_serializer.save()
            assessment_data["vital_signs"] = vital_signs_object.vital_signs_id

            assessment_data["changes_in_condition"] = self.add_condition_changes(assessment_data["changes_in_condition"])

            """
            Process list type data fields into strings
            """
            assessment_data["priority_problems"] = self.join_list(assessment_data["priority_problems"])
            assessment_data["interventions"] = self.join_list(assessment_data["interventions"])
            assessment_data["recommendations"] = self.join_list(assessment_data["recommendations"])

            """
            Create New Client Assessment object
            """
            existing_case_client_serializer = ExistingCaseClientAssessmentSerializer(data=assessment_data)
            if existing_case_client_serializer.is_valid():
                existing_case_client_object = existing_case_client_serializer.save()

                client_assessment_serializer = CommunityClientAssessmentSerializer(data={
                    "community_paramedic": request_data.get('community_paramedic'),
                    "client": request_data.get("client"),
                    "client_status": request_data.get("client_status"),
                    "existing_case_client_assessment": existing_case_client_object.assessment_id
                })

                if client_assessment_serializer.is_valid():
                    client_assessment_serializer.save()
                    return Response("Successfully added client assessment record.",
                                    status=status.HTTP_201_CREATED)
                else:
                    print(client_assessment_serializer.errors)
                    return Response("Failed to create client assessment record.",
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                print(existing_case_client_serializer.errors)
                return Response("Invalid client assessment data provided.",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid vital signs data in the assessment.",
                            status=status.HTTP_400_BAD_REQUEST)
