# Appointment Scheduler

This application helps you to schedule appointments with your clients. It is a simple application that allows any client
to schedule an appointment for a service.

## Model Structure

The application has 6 models:

- [Service](models.md#service)
- [Appointment Request](models.md#appointmentrequest)
- [Appointment](models.md#appointment)
- [Config](models.md#config)
- [PaymentInfo](models.md#paymentinfo)
- [EmailVerificationCode](models.md#emailverificationcode)

### Service

The service model is used to define the services that you offer. It has the following fields:

- name: The name of the service
- description: A description of the service
- duration: The duration of the service (Duration field)
- price: The price of the service
- image: An image of the service

### Appointment Request

The appointment request model is used to define the appointment requests that your clients make. It has the following
fields:

- date: The date of the appointment request
- start_time: The start time of the appointment request
- end_time: The end time of the appointment request
- service: The service that the appointment request is for
- id_request: The id of the appointment request

The appointment request is used to create the appointment. An appointment is considered having more information than
that, and since we don't want to overload the appointment model, we use the appointment request to store all
the information about the appointment.

### Appointment

The appointment model is used to define the last step in the appointment scheduling. It has the following fields:

- client: The client that made the appointment
- appointment_request: The appointment request that the appointment is based on
- phone: The phone number of the client
- address: The address of the client
- want_reminder: A boolean field that indicates if the client wants a reminder
- additional_info: Additional information about the appointment
- paid: A boolean field that indicates if the appointment has been paid fully
- amount_paid: The amount paid for the appointment if partial payment is enabled
- id_request: The id of the appointment request

### Config

The config model is used to define the configuration of the application. It has the following fields:

- slot_duration: The duration of each slot in the calendar
- lead_time: The time of the day that the calendar starts
- finish_time: The time of the day that the calendar ends
- appointment_buffer_time: Time between now and the first available slot for the current day (doesn't affect tomorrow).
- website_name: The name of the website

### PaymentInfo

The PaymentInfo model is used to represent payment information for an appointment. It has the following fields:

- appointment: A foreign key reference to the Appointment model

The model provides several methods to access related appointment details, such as service name, price, currency, client
name, and email.
It also includes a method to update the payment status.

### EmailVerificationCode

The EmailVerificationCode model is used to represent an email verification code for a user when the email already exists
in the database.
It has the following fields:

- user: A foreign key reference to the user model defined in `APPOINTMENT_CLIENT_MODEL`
- code: A randomly generated 6-character alphanumeric code

The model includes a class method to generate a new verification code for a user.

## Configuration

In your Django project's settings.py, you can override the default values for the appointment scheduler:

```python
APPOINTMENT_CLIENT_MODEL = 'auth.User'  # file.Model
APPOINTMENT_BASE_TEMPLATE = 'base_templates/base.html'
APPOINTMENT_WEBSITE_NAME = 'Website'
APPOINTMENT_PAYMENT_URL = None
APPOINTMENT_THANK_YOU_URL = None
APPOINTMENT_SLOT_DURATION = 30  # minutes
APPOINTMENT_LEAD_TIME = (9, 0)  # (hour, minute) 24-hour format
APPOINTMENT_FINISH_TIME = (16, 30)  # (hour, minute) 24-hour format
```

