<script>
    import Card from "$lib/Card.svelte";
    let card_num;
    let cards; 

    async function get_card() {
        const data = await (await fetch(`http://localhost:80/cards/${card_num}`)).json()
        cards = data;
        cards = cards;
        card_num = "";
    }
</script>

<svelte:head>
    <title>DigiDigits</title>
</svelte:head>

<body class="bg-blue-300">
    <div class="flex flex-col justify-center items-center">
        <form class="flex flex-col" on:submit={get_card}>
            <input type="text" class="border-2 border-black rounded-lg mt-10 p-1.5" placeholder="card num here" bind:value={card_num}>
            <input type="submit" value="search" class="cursor-pointer border-2 border-black w-fit mx-auto p-2 mt-2 bg-white font-bold rounded-lg">
        </form>
        <div class="grid grid-cols-[repeat(auto-fill,minmax(300px,1fr))] gap-4 w-full p-4 auto-rows-fr justify-items-center">
            {#if cards}
                {#each cards as card}
                    <Card 
                    num={card.card_num}
                    name={card.card_name} 
                    id={card.id} 
                    price={card.market_price}
                    pack={card.pack}
                    />
                {/each}
            {/if}
        </div>
    </div>
</body>