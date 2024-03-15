from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .donationSerializer import DonationSerializer
from rest_framework.permissions import AllowAny
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime



class DonationApiViewSet(ModelViewSet):
    queryset = Donation.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



def DonationsExportToCsv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Datos_Donaciones.csv"'
    #Retrieve data from your model
    queryset = Donation.objects.all()

    #Create a CSV writer object
    writer = csv.writer(response)

    writer.writerow(
        ["Cantidad", " Frecuencia", " QuotaExtensionDocument", " Titular", " Fecha"]
    )

    #Write data rows
    for donation in queryset:
        writer.writerow(
            [
                donation.quantity,
                donation.frequency,
                donation.quota_extension_document,
                donation.holder,
                donation.date,
            ]
        )

    return response

def obtainDataFromRequest (request):
    #Get data from request
    startDate_str = request.GET.get('startdate')
    endDate_str = request.GET.get('enddate')
    actualDate= datetime.now().date()
    partner_str = request.GET.get('partner')

    #Comprobe if data exist
    if not startDate_str:
        startDate = None
    else:
        startDate = datetime.strptime(startDate_str, '%Y-%m-%d')
    if not endDate_str:
        endDate = None
    else:
        endDate = datetime.strptime(endDate_str, '%Y-%m-%d')
    if not partner_str:
        partner = 0
        userOfPartner = None
    else:
        partner = partner_str
        userOfPartner = User.objects.filter(partner=partner).first()

    #Filter donations
    if startDate is not None and partner == 0:
        queryset = Donation.objects.filter(date__gte=startDate, date__lte=endDate)
    else:
        if partner != 0 and startDate is not None:
            queryset = Donation.objects.filter(date__gte=startDate, date__lte=endDate, partner=partner)
        else:
            if partner !=0 and startDate is None:
                queryset = Donation.objects.filter(partner=partner)
            else:
                queryset= Donation.objects.all()
            
    if startDate is None and partner == 0:
        filename = "Reporte de donaciones global."
    else:
        if partner != 0:
            if startDate is None:
                filename = f"Reporte_de_donaciones_de_{userOfPartner.name}."
            else:
                filename = f"Reporte_de_donaciones_entre_{startDate_str}_y_{endDate_str}_de_{userOfPartner.name}."
        else:
            filename = f"Reporte_de_donaciones_entre_{startDate_str}_y_{endDate_str}."
    return startDate_str, endDate_str, actualDate, startDate, endDate, partner, userOfPartner, queryset, filename

def DonationsExportToPdf(request):
    startDate_str, endDate_str, actualDate, startDate, partner, userOfPartner, queryset, filename = obtainDataFromRequest(request)
    #Response Object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}.pdf'
    styles = getSampleStyleSheet()

    #This is the PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    #Create a Story list to hold elements
    Story = []

    #Add cover page elements
    logoPath = 'static/images/logo.png'
    logo = Image(logoPath, width=200, height=100)
    if partner == 0:
        title = "Reporte de donaciones"
    else:
        title=f"Reporte de donaciones de {userOfPartner.name}"
    startDateText = f"Fecha de inicio de los datos: {startDate_str}"
    endDateText = f"Fecha de fin de los datos: {endDate_str}"
    actualDateText = f"Fecha actual: {actualDate}"

    if startDate is None:
        cover_elements = [logo, Spacer(1, 12), Paragraph(title, styles['Title']), Spacer(1, 12), 
                      Paragraph(actualDateText, styles['Normal'])]
    else:
        cover_elements = [logo, Spacer(1, 12), Paragraph(title, styles['Title']), Spacer(1, 12),
                      Paragraph(actualDateText, styles['Normal']), Spacer(1, 6),
                      Paragraph(startDateText, styles['Normal']), Spacer(1, 6),
                      Paragraph(endDateText, styles['Normal'])]
        
    #Add cover elements to the Story
    Story.extend(cover_elements)
    #Separation for the table
    Story.append(Spacer(1, 50))
    table_data = [['Cantidad', 'Frecuencia', 'Titular', 'Fecha']]

    for donation in queryset:
        table_data.append([donation.quantity, donation.frequency, donation.holder, donation.date])

    #Create a table 
    table = Table(table_data)

    #Table style
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    #Table to Story
    Story.append(table)
    doc.build(Story)

    return response

def DonationsExportToExcel(request):
    data = obtainDataFromRequest(request)
    filename = data[-1]
    queryset = data[-2]
        
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'

    #Create a new Excel workbook
    workbook = Workbook()
    sheet = workbook.active

    header_row = ['Cantidad', 'Frecuencia', 'QuotaExtensionDocument', 'Titular', 'Fecha']
    sheet.append(header_row)

    for donation in queryset:
        data_row = [donation.quantity, donation.frequency, donation.quota_extension_document.name, donation.holder, donation.date]
        sheet.append(data_row)

    # Save the workbook to the response
    workbook.save(response)

    return response