from django.urls import reverse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import FrontPage
from store.models import UserStore
from produk.models import (
    Kategori,
    WarnaProduk,
    TipeProduk,
    Expedisi,
    GambarProduk,
    Produk
)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class Jual(FrontPage):
    def get(self, request):
        user = UserStore.objects.filter(users_id=request.user.id)
        if user.exists():
            user = user.first()
            if user.is_active_store is False:
                return redirect(reverse("profile"))
        kategori = Kategori.objects.all()
        typeproduk = TipeProduk.objects.all()
        warnaproduk = WarnaProduk.objects.all()
        expedisi = Expedisi.objects.all()
        return render(
            request,
            "jualpage.html",
            {
                "kategori": kategori,
                "typeproduk": typeproduk,
                "warnaproduk": warnaproduk,
                "ekspedisi": expedisi,
            },
        )

    def post(self, request):
        refinput = request.POST
        reffile = request.FILES
        store = None
        try:
            store = UserStore.objects.get(users__pk=request.user.id)
        except Exception as e:
            print(e)
            store = UserStore.objects.create(
                users=request.user, nama=request.user.username
            )

        try:
            produk = Produk.objects.get(
                store__id=store.id, nama=refinput.get("nama", "")
            )
            messages.error(request, "Produk sudah ada")
        except Exception as e:
            print(e)
            produk = Produk.objects.create(
                store=store,
                nama=refinput.get("nama", ""),
                harga=refinput.get("harga", 1),
                detail=refinput.get("deskripsi", "-"),
                stok_produk=refinput.get("stok", 1),
                berat=refinput.get("berat"),
                lebar=refinput.get("lebar"),
                cross_boarder=refinput.get("lintas_negara", False),
            )
            for k in refinput.getlist("kategori"):
                kateg = Kategori.objects.filter(pk=k).first()
                produk.kategori.add(kateg)

            for k in refinput.getlist("warna"):
                try:
                    warnaa = WarnaProduk.objects.filter(pk=k).first()
                except Exception as e:
                    print(e)
                    warnaa = WarnaProduk.objects.filter(nama=k).first()
                if warnaa:
                    produk.warna.add(warnaa)
                else:
                    warnaa = WarnaProduk.objects.create(nama=k)
                    produk.warna.add(warnaa)

            tipes = TipeProduk.objects.filter(pk=refinput.get("tipe")).first()
            produk.tipe.add(tipes)
            # print(reffile.get("gambar"))
            for reffiles in reffile.getlist("gambar"):
                GambarProduk.objects.create(
                    produk=produk, nama=refinput.get("nama", "-"), gambar=reffiles
                )
        messages.success(request, "Produk Berhasil disimpan")
        return redirect(reverse("jual"))
