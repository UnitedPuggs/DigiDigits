<script>
    export let name;
    export let id;
    export let price;
    export let pack;
    export let num;
</script>

<a href="/card/{id}" class="w-fit">
<div class="bg-white flex flex-col p-2 border-2 border-black rounded-md transition-all duration-100 ease-linear hover:translate-x-2 hover:no-shadow box-shadow justify-center items-center hover:scale-95 w-72 h-84">
    <div class="w-48 h-64 border border-black bg-black rounded-lg">
        <img src="https://images.digimoncard.io/images/cards/{num}.jpg" alt="card back" class="w-full h-full object-contain" />
    </div>
    <div class="flex flex-col mt-auto mb-0 text-center">
        <span class="text-lg"><strong>Name:</strong> {name}</span>
        <span><strong>Current Price:</strong> ${price}</span>
        <span class="h-12 overflow-y-auto text-ellipsis text-sm"><strong>Pack:</strong> {pack}</span>
    </div>
</div>
</a>