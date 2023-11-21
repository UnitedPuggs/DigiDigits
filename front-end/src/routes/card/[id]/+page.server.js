export async function load({ params, fetch }) {
    const card = await (await fetch(`http://localhost:80/cards/info/${params.id}`)).json()
    const market = await (await fetch(`http://localhost:80/cards/market/${params.id}`)).json();
    return { card, market }
}