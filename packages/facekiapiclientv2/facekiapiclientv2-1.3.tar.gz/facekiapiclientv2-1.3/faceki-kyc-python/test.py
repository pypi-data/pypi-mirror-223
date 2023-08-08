from client import FacekiAPIClientV2


facekiClinet = FacekiAPIClientV2("71giup851atf12nsuv6lbtbq1n","2m4nsbkm8eas1qm7d8okn8vu1bt9pb1fvlmbmia1oa38hbv909t")

# print(facekiClinet.generateKYCLink(0,None,"https://google.com",False,True))
print(facekiClinet.getKYCrecordsByLink("5d7503f8-8e0e-4e39-8b00-0bd4923e287c"))
