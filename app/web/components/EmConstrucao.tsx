// Tela ainda não montada: mostra o título e quando ela entra. O desenho já existe no protótipo.
export function EmConstrucao({ titulo, descricao, quando }: { titulo: string; descricao: string; quando: string }) {
  return (
    <>
      <div>
        <h1>{titulo}</h1>
        <p className="sub">{descricao}</p>
      </div>
      <div className="card empty">
        <b>Esta tela entra em {quando}</b>
        <p>O desenho já está pronto no protótipo. Assim que ela for montada, aparece aqui com os dados da sua clínica.</p>
      </div>
    </>
  );
}
