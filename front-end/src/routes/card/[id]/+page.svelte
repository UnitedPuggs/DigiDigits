<script>
    import { Line } from 'svelte-chartjs'
    import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale} from 'chart.js'
    export let data;

    ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale)
    $: card = data.card[0]
    $: market = data.market
    
    const market_data = data.market;
    let labels = market_data.map(x => x.date).reverse();
    let price_data = market_data.map(x => x.market_price).reverse();

    const chart_data = {
        labels: labels,
        datasets: [
            {
            label: 'Price in $',
            lineTension: 0.3,
            backgroundColor: 'rgba(225, 204, 230, .3)',
            borderColor: 'rgb(94, 92, 242)',
            borderJoinStyle: 'miter',
            pointBorderColor: 'rgb(0, 0, 0)',
            pointBackgroundColor: 'rgb(255, 255, 255)',
            pointBorderWidth: 5,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgb(0, 0, 0)',
            pointHoverBorderColor: 'rgba(220, 220, 220, 1)',
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: price_data,
            },
        ],
    };
</script>

<svelte:head>
    <title>DigiDigits | {card.card_name}</title>
</svelte:head>

<a href="/" class="text-3xl hover:opacity-80">&lt-</a>
<div class="flex bg-white h-screen border-2 border-black">
    <div class="flex flex-col text-center justify-center items-center w-1/2 border-r-2 border-black">
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="bg-black border-2 border-black rounded-lg w-fit mb-4 transition-all duration-300 hover:scale-105">
            <img src="https://images.digimoncard.io/images/cards/{card.card_num}.jpg" alt="card back" class="object-contain drop-shadow-2xl" />
        </div>
        <span class="text-xl font-bold">Card Name</span>
        <span>{card.card_name}</span>
        <span class="text-xl font-bold">Pack</span>
        <span>{card.pack}</span>
        <span class="text-xl font-bold">Rarity</span>
        <span>{card.rarity}</span>
    </div>
    <section class="flex flex-col p-2 w-1/2 items-center justify-center">
        <span class="font-bold lg:text-4xl">Last collected on {market[0].date}</span>
        <!-- this is where the graphs and price data would go -->
        <span class="lg:text-2xl"><strong>Current Price:</strong> ${market[0].market_price}</span>
        <Line
            data={chart_data}
            options={{ maintainAspectRatio: true }}
        />
    </section>
</div>