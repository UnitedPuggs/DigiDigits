<script>
    let card_num;
    let cards; 

    async function get_card() {
        const req = await fetch(`http://localhost:80/card-info/${card_num}`)
        const res = await req.json()
        cards = res;
        cards = cards;
        card_num = "";
    }
</script>

<body>
    <div class="flex flex-col justify-center items-center">
        <form class="flex flex-col">
            <input type="text" class="border-2 border-black rounded-lg mt-10 p-1.5" placeholder="card num here" bind:value={card_num}>
            <button on:click={get_card}>submit</button>
        </form>
        <div class="flex flex-col gap-2">
            {#if cards}
                {#each cards as card}
                    <span>{card.card_name} | {card.rarity} | {card.pack}</span>
                {/each}
            {/if}
        </div>
    </div>
</body>