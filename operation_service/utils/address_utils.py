def address_as_json(address):
    name = ""
    if address.client.client_name:
        name = str(address.client.client_name)

    if address.address_line1:
        address_line1 = str(address.address_line1)
    else:
        address_line1 = ""

    if address.area:
        area = str(address.area)
    else:
        area = ""

    if address.city:
        city = str(address.city)
    else:
        city = ""

    if address.country:
        country = address.country
    else:
        country = "IN"

    if address.pin_code:
        pin_code = str(address.pin_code)
    else:
        pin_code = ""

    if address.state:
        state = str(address.state)
    else:
        state = ""

    address_line_one = address_line1 + " - " + area + " - " + city
    return dict(
        Name=name, Country=country,
        Pincode=pin_code,
        State=state, AddressLine1=address_line_one,
        area=area
    )