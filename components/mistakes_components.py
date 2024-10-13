import pandas as pd
import plotly.express as px
import streamlit as st
import umap
from sklearn.cluster._hdbscan import hdbscan
from sklearn.feature_extraction.text import TfidfVectorizer

from services.results_service import ResultsService
from utils.preprocess import preprocess_text

EPS = 0.5
MIN_SAMPLES = 3


results_service = ResultsService()


def render_mistakes():
    # Шаг 02: Загрузка тестовых данных
    reasons = [
        "Не соответствует конструкция тормозного оборудования требованиям устойчивости к вибрациям.",
        "Тормозные компоненты не защищены от коррозии и воздействия агрессивных сред.",
        "Отсутствует сертификация тормозной системы согласно международным стандартам.",
        "Неправильная установка тормозных дисков, что приводит к неравномерному износу.",
        "Используются материалы низкого качества, снижающие долговечность тормозных элементов.",
        "Система автоматического торможения не реагирует на снижение давления в тормозной системе.",
        "Недостаточная эффективность резервной тормозной системы при полной нагрузке.",
        "Отсутствует документальная информация о проведенных испытаниях тормозной системы.",
        "Сигналы неисправности тормозной системы появляются с задержкой более 10 мс.",
        "Тормозные колодки содержат запрещенные химические вещества, вредные для здоровья.",
        "Отсутствует система контроля износа тормозных дисков в реальном времени.",
        "Рабочая тормозная система не обеспечивает стабильное тормозное усилие при различных скоростях.",
        "Система стояночного тормоза не активируется автоматически при парковке на наклонной поверхности.",
        "Отсутствует возможность самостоятельной регулировки тормозного усилия водителем.",
        "Тормозная система перегревается при длительном использовании, что снижает ее эффективность.",
        "Неисправность в системе гидравлического привода тормозов не обнаруживается своевременно.",
        "Система торможения не соответствует требованиям по шуму и вибрации.",
        "Отсутствует резервная электронная система управления тормозами.",
        "Тормозные цилиндры не обеспечивают достаточную герметичность, приводя к утечкам тормозной жидкости.",
        "Отсутствует регулярная возможность технического обслуживания и проверки состояния тормозной системы.",
        "Отсутствует документальное подтверждение соответствия тормозной системы требованиям регламента.",
        "Тормозные накладки содержат асбест, что противоречит требованиям.",
        "Магнитные поля влияют на эффективность тормозной системы.",
        "Сигнал обнаружения неисправности тормозной системы не прерывает сигнал управления в пределах 10 мс.",
        "Рабочая тормозная система не позволяет водителю тормозить без отрыва рук от руля.",
        "Резервная тормозная система не обеспечивает остановку транспортного средства при отказе рабочей системы.",
        "Стояночная тормозная система не удерживает транспортное средство на подъеме.",
        "Отсутствуют независимые органы управления рабочим и стояночным тормозами.",
        "Система тормозов подвержена коррозии и старению из-за несоблюдения требований по материалам.",
        "Тормозное оборудование не обеспечивает надежное торможение при воздействии вибраций.",
        "Рабочая тормозная система не позволяет регулировать тормозное усилие.",
        "Резервная тормозная система не функционирует при отказе рабочей системы.",
        "Стояночная тормозная система не может удерживать транспортное средство на крутых подъемах.",
        "Тормозная система не противостоит коррозии и старению, что приводит к снижению ее эффективности.",
        "Отсутствуют независимые органы управления рабочим и стояночным тормозами.",
        "Связь между органом управления рабочим тормозом и приводами ухудшается после эксплуатации.",
        "Система тормозов не имеет достаточных средств защиты от простой несанкционированной модификации режима работы.",
        "Тормозное оборудование не сертифицировано согласно регламенту, что приводит к его несоответствию техническим требованиям.",
        "Магнитные поля оказывают негативное воздействие на эффективность тормозной системы.",
        "Тормозные накладки содержат запрещенные материалы, такие как асбест.",
        "Сигнал выявления неисправности тормозной системы не прерывает сигнал управления в пределах 10 мс.",
        "Тормозное оборудование не позволяет водителю осуществлять торможение, не отрывая рук от руля.",
        "Система автоматического торможения не может отключаться во время испытаний на официальное утверждение типа тормозной системы.",
        "Рабочая тормозная система не обеспечивает надежное торможение при различных нагрузках и скоростях транспортного средства.",
        "Отсутствует возможность оценки износа элементов рабочей тормозной системы во время периодических технических проверок.",
        "Тормозное оборудование не выдерживает максимального тормозного усилия на динамометрическом стенде.",
        "Резервная тормозная система не обеспечивает остановку транспортного средства на разумном расстоянии при отказе рабочей системы.",
        "Стояночная тормозная система не поддерживает рабочие части в заторможенном положении при отсутствии водителя.",
        "Тормозная система использует материалы, подверженные значительным деформациям при нормальной эксплуатации.",
        "Тормозное оборудование не оснащено по крайней мере двумя независимыми органами управления, доступными водителю.",
        "Система торможения не имеет механизма автоматического восстановления после снятия нагрузки с органа управления.",
        "Тормозные цилиндры и их поршни не обеспечивают требуемой надежности и долговечности.",
        "Тормозная система не может обеспечить требуемую эффективность торможения при работе в условиях повышенной вибрации.",
        "Сигнальное устройство системы торможения не функционирует корректно при возникновении неисправности.",
        "Тормозная система не предоставляет водителю возможность визуального подтверждения режима функционирования тормозов после включения питания."
    ]

    if not reasons:
        st.warning("No data for cluster.")
        return


    # Preprocess
    cleaned_reasons = [preprocess_text(reason) for reason in reasons]

    # Vectorize
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    vectors = vectorizer.fit_transform(cleaned_reasons)

    # HDBSCAN
    hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=3, metric='cosine')
    cluster_labels = hdbscan_model.fit_predict(vectors.toarray())

    # UMAP
    reducer = umap.UMAP(n_neighbors=MIN_SAMPLES, min_dist=0.1, metric='cosine')
    embedding_2d = reducer.fit_transform(vectors)

    df = pd.DataFrame({
        'reason': reasons,
        'cluster': cluster_labels,
        'UMAP1': embedding_2d[:, 0],
        'UMAP2': embedding_2d[:, 1]
    })

    # Clusters
    no_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    noise = list(cluster_labels).count(-1)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<h1 style='text-align: center; color: #FFFFFF; font-size: 16px'>Total reasons: {len(reasons)}</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h1 style='text-align: center; color: #FFFFFF; font-size: 16px'>Total clusters {no_clusters}</h1>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h1 style='text-align: center; color: #FFFFFF; font-size: 16px'>Noise points {noise}</h1>", unsafe_allow_html=True)

    # Plotly
    unique_clusters = sorted(df['cluster'].unique())
    colors = px.colors.qualitative.Plotly
    color_map = {cluster: colors[i % len(colors)] for i, cluster in enumerate(unique_clusters)}
    df['color'] = df['cluster'].map(color_map)

    fig = px.scatter(
        df, x='UMAP1', y='UMAP2',
        color=df['cluster'].astype(str),
        hover_data=['reason'],
        title="Clusterization of reasons with DBSCAN + UMAP",
        labels={'UMAP1': 'UMAP 1', 'UMAP2': 'UMAP 2', 'color': 'Cluster'}
    )

    fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))
    fig.update_layout(legend_title_text='Cluster')

    st.plotly_chart(fig, use_container_width=True)

    # Clusters
    st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Clusters of reasons</h1>", unsafe_allow_html=True)
    for cluster in unique_clusters:
        cluster_reasons = df[df['cluster'] == cluster]['reason'].tolist()

        if cluster == -1:
            expander = st.expander(f"Noise (Cluster {cluster}) - ({len(cluster_reasons)})")
        else:
            expander = st.expander(f"Cluster {cluster} - ({len(cluster_reasons)})")

        reasons = ""
        for reason in cluster_reasons:
            reasons += f"- {reason}\n"
        expander.write(reasons)
