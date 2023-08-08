from typing import Union, List
import pandas as pd
from sqlalchemy import select
from .constants import (
    SECOND_STRATEGY_PPW_MAP,
    STRATEGY_PPW_MAP,
    THIRD_STRATEGY_PPW_MAP,
    AUM_MAPPER,
    FUNDTYPE_PPW_MAP,
)
from .utils import DBConnection


class Inquirer:
    def __init__(self, db: DBConnection) -> None:
        self.db = db
        self.conn = self.db.conn

    # 常用单表查询接口及筛选条件
    def _get_company_info(
        self,
        company_type=1,  # 管理人类型,默认1私募证券类
        company_name: str = None,  # 管理人名称,模糊查询
        company_ids: Union[str, List[str]] = None,  # 排排网管理人id批量查询
        register_numbers: Union[str, List[str]] = None,  # 协会备案id批量查询
        est_start: Union[str, pd.Timestamp] = None,  # 成立起始时间
        est_end: Union[str, pd.Timestamp] = None,  # 成立终止时间
        province: str = None,
        city: str = None,
        aum_min: int = None,
        aum_max: int = None,
    ):
        """
        私募管理人基本信息表
        pvn_company_info
        """
        try:
            t_company_info = self.db.tables["smppw.pvn_company_info"]
        except:
            t_company_info = self.db.tables["company_info"]

        if isinstance(company_ids, str):
            company_ids = [company_ids]
        if isinstance(register_numbers, str):
            register_numbers = [register_numbers]
        if isinstance(est_start, str):
            est_start = pd.Timestamp(est_start)
        if isinstance(est_end, str):
            est_end = pd.Timestamp(est_end)

        if aum_min is not None:
            if aum_min not in [0, 5, 10, 20, 50, 100]:
                raise ValueError("资管规模下限必须为0,5,10,20,50,100中的一个")
        if aum_max is not None:
            if aum_max not in [5, 10, 20, 50, 100]:
                raise ValueError("资管规模上限必须为5,10,20,50,100中的一个")
        aum_min = AUM_MAPPER.get(aum_min, 1)
        aum_max = AUM_MAPPER.get(aum_max, 7)

        if aum_max <= aum_min:
            raise ValueError("资管规模上限必须大于下限")

        if aum_max == 7 and aum_min == 1:
            aum_args = None
        else:
            aum_args = tuple(range(aum_min, aum_max))

        stmt = select(t_company_info).where(
            t_company_info.c.company_type == company_type
        )

        if company_name is not None:
            stmt = stmt.where(
                t_company_info.c.company_short_name.like(f"%{company_name}%")
            )

        if company_ids is not None:
            stmt = stmt.where(t_company_info.c.company_id.in_(company_ids))

        if register_numbers is not None:
            stmt = stmt.where(t_company_info.c.register_number.in_(register_numbers))

        if province is not None:
            stmt = stmt.where(t_company_info.c.province.like(f"%{province}%"))

        if city is not None:
            stmt = stmt.where(t_company_info.c.city.like(f"%{city}%"))

        if est_start is not None:
            stmt = stmt.where(t_company_info.c.establish_date > est_start)

        if est_end is not None:
            stmt = stmt.where(t_company_info.c.establish_date < est_end)

        if aum_args is not None:
            stmt = stmt.where(t_company_info.c.company_asset_size.in_(aum_args))

        return pd.read_sql(stmt, self.conn, index_col="company_id")

    def _get_fund_info(
        self,
        fund_name: str = None,  # 单产品名称,模糊查询
        fund_type: Union[int, List[int]] = None,  # 产品类型查询
        company_ids: Union[str, List[str]] = None,  # 使用排排网管理人id批量查询
        fund_ids: Union[str, List[str]] = None,  # 使用排排网产品id批量查询
        register_numbers: Union[str, List[str]] = None,  # 使用协会备案编码批量查询
        est_start: Union[str, pd.Timestamp] = None,  # 产品最早成立时间
        est_end: Union[str, pd.Timestamp] = None,  # 产品最晚成立时间
    ):
        """
        私募产品基本信息表
        pvn_fund_info
        """
        try:
            t_fund_info = self.db.tables["smppw.pvn_fund_info"]
        except:
            t_fund_info = self.db.tables["fund_info"]

        if isinstance(company_ids, str):
            company_ids = [company_ids]
        if isinstance(fund_ids, str):
            fund_ids = [fund_ids]
        if isinstance(fund_type, int):
            fund_type = [fund_type]
        if isinstance(register_numbers, str):
            register_numbers = [register_numbers]

        if isinstance(est_start, str):
            est_start = pd.Timestamp(est_start)
        if isinstance(est_end, str):
            est_end = pd.Timestamp(est_end)

        stmt = select(t_fund_info)

        if fund_name is not None:
            stmt = stmt.where(t_fund_info.c.fund_short_name.like(f"%{fund_name}%"))
        if fund_type is not None:
            stmt = stmt.where(t_fund_info.c.fund_type.in_(fund_type))
        if company_ids is not None:
            stmt = stmt.where(t_fund_info.c.trust_id.in_(company_ids))
        if fund_ids is not None:
            stmt = stmt.where(t_fund_info.c.fund_id.in_(fund_ids))
        if register_numbers is not None:
            stmt = stmt.where(t_fund_info.c.register_number.in_(register_numbers))

        if est_start is not None:
            stmt = stmt.where(t_fund_info.c.inception_date > est_start)
        if est_end is not None:
            stmt = stmt.where(t_fund_info.c.inception_date < est_end)

        return pd.read_sql(stmt, self.conn, index_col="fund_id")

    def _get_fund_status(
        self,
        fund_ids: Union[str, List[str]] = None,  # 使用排排网产品id批量查询
        fund_status: Union[int, List[int]] = None,  # 产品状态筛选
    ):
        """
        私募产品状态表
        pvn_fund_info
        """
        try:
            t_fund_status = self.db.tables["smppw.pvn_fund_status"]
        except:
            t_fund_status = self.db.tables["fund_status"]

        if isinstance(fund_ids, str):
            fund_ids = [fund_ids]
        if isinstance(fund_status, int):
            fund_status = [fund_status]

        stmt = select(t_fund_status).where(t_fund_status.c.isvalid == 1)

        if fund_ids is not None:
            stmt = stmt.where(t_fund_status.c.fund_id.in_(fund_ids))
        if fund_status is not None:
            stmt = stmt.where(t_fund_status.c.fund_status.in_(fund_status))

        return pd.read_sql(stmt, self.conn, index_col="fund_id")

    def _get_fund_strategy(
        self,
        fund_ids: Union[str, List[str]] = None,  # 使用排排网产品id批量查询
        first_strategy: Union[str, List[str]] = None,  # 一级策略类别
        second_strategy: Union[str, List[str]] = None,  # 二级策略类别
        third_strategy: Union[str, List[str]] = None,  # 三级策略类别
    ):
        """
        私募产品策略表
        pvn_fund_strategy
        """
        try:
            t_fund_strategy = self.db.tables["smppw.pvn_fund_strategy"]
        except:
            t_fund_strategy = self.db.tables["strategy"]

        if isinstance(fund_ids, str):
            fund_ids = [fund_ids]
        if isinstance(first_strategy, str):
            first_strategy = [first_strategy]
        if isinstance(second_strategy, str):
            second_strategy = [second_strategy]
        if isinstance(third_strategy, str):
            third_strategy = [third_strategy]

        stmt = select(t_fund_strategy).where(t_fund_strategy.c.isvalid == 1)

        if fund_ids is not None:
            stmt = stmt.where(t_fund_strategy.c.fund_id.in_(fund_ids))
        if first_strategy is not None:
            stmt = stmt.where(t_fund_strategy.c.first_strategy.in_(first_strategy))
        if second_strategy is not None:
            stmt = stmt.where(t_fund_strategy.c.second_strategy.in_(second_strategy))
        if third_strategy is not None:
            stmt = stmt.where(t_fund_strategy.c.third_strategy.in_(third_strategy))

        return pd.read_sql(stmt, self.conn, index_col="fund_id")

    def _get_fund_manager(
        self,
        fund_ids: Union[str, List[str]] = None,  # 使用排排网产品id批量查询
        fund_manager_ids: Union[str, List[str]] = None,  # 使用排排网基金经理id批量查询
    ):
        """
        私募产品基金经理关联表
        pvn_fund_manager_mapping
        """
        try:
            t_fund_manager = self.db.tables["smppw.pvn_fund_manager_mapping"]
        except:
            t_fund_manager = self.db.tables["fund_manager_map"]

        if isinstance(fund_ids, str):
            fund_ids = [fund_ids]
        if isinstance(fund_manager_ids, str):
            fund_manager_ids = [fund_manager_ids]

        stmt = select(t_fund_manager).where(t_fund_manager.c.isvalid == 1)

        if fund_ids is not None:
            stmt = stmt.where(t_fund_manager.c.fund_id.in_(fund_ids))
        if fund_manager_ids is not None:
            stmt = stmt.where(t_fund_manager.c.fund_manager_id.in_(fund_manager_ids))

        return pd.read_sql(stmt, self.conn, index_col="fund_id")

    def _get_manager(
        self,
        name: str = None,  # 基金经理姓名,模糊查询
        manager_ids: Union[str, List[str]] = None,  # 使用排排网基金经理产品id批量查询
    ):
        """
        基金经理表
        pvn_personnel_info
        """
        try:
            t_manager_info = self.db.tables["smppw.pvn_personnel_info"]
        except:
            t_manager_info = self.db.tables["manager_info"]

        if isinstance(manager_ids, str):
            manager_ids = [manager_ids]

        stmt = select(t_manager_info).where(t_manager_info.c.isvalid == 1)

        if name is not None:
            stmt = stmt.where(t_manager_info.c.personnel_name.like(f"%{name}%"))
        if manager_ids is not None:
            stmt = stmt.where(t_manager_info.c.personnel_id.in_(manager_ids))

        return pd.read_sql(stmt, self.conn, index_col="fund_id")

    def _get_net_values(
        self,
        ids: Union[str, List[str]] = None,  # 使用排排网产品id批量查询
        price_date_min: Union[str, pd.Timestamp] = None,  # 净值起始区间
        price_date_max: Union[str, pd.Timestamp] = None,  # 净值起始区间
    ):
        """
        产品净值查询
        pvn_nav
        """
        try:
            t_net_values = self.db.tables["smppw.pvn_nav"]
        except:
            t_net_values = self.db.tables["net_values"]

        if isinstance(ids, str):
            ids = [ids]

        if isinstance(price_date_min, str):
            price_date_min = pd.Timestamp(price_date_min)
        if isinstance(price_date_max, str):
            price_date_max = pd.Timestamp(price_date_max)

        stmt = select(t_net_values).where(t_net_values.c.isvalid == 1)

        if ids is not None:
            stmt = stmt.where(t_net_values.c.fund_id.in_(ids))

        if price_date_min is not None:
            stmt = stmt.where(t_net_values.c.price_date > price_date_min)
        if price_date_max is not None:
            stmt = stmt.where(t_net_values.c.price_date < price_date_max)

        return pd.read_sql(stmt, self.conn, index_col="fund_id")

    def _get_qr_report(
        self,
        company_name: str = None,  # 使用公司名称模糊查询
        company_ids: Union[str, List[str]] = None,  # 使用排排网公司id批量查询
        register_numbers: Union[str, List[str]] = None,  # 使用协会登记编码批量查询
    ):
        """
        公司定性报告信息
        pvn_qr_qualitative_report
        """
        t_qr_report = self.db.tables["smppw.pvn_qr_qualitative_report"]

        if isinstance(company_ids, str):
            company_ids = [company_ids]
        if isinstance(register_numbers, str):
            register_numbers = [register_numbers]

        stmt = select(t_qr_report)

        if company_name is not None:
            stmt = stmt.where(t_qr_report.c.organization_name.like(f"%{company_name}%"))
        if company_ids is not None:
            stmt = stmt.where(t_qr_report.c.company_id.in_(company_ids))
        if register_numbers is not None:
            stmt = stmt.where(register_numbers.c.register_number.in_(register_numbers))

        return pd.read_sql(stmt, self.conn, index_col="id")

    def _get_qr_summary(
        self,
        qr_ids: Union[str, List[str]] = None,  # 使用排排网尽调报告id批量查询
    ):
        """
        尽调报告简评
        pvn_qr_summary_desc
        """
        t_qr_summary = self.db.tables["smppw.pvn_qr_summary_desc"]

        if isinstance(qr_ids, float):
            qr_ids = [qr_ids]

        stmt = select(t_qr_summary)
        if qr_ids is not None:
            stmt = stmt.where(t_qr_summary.c.qr_id.in_(qr_ids))

        return pd.read_sql(stmt, self.conn, index_col="id")

    # 无此表
    # def _get_company_grow_history(
    #     self,
    #     company_name: str = None,  # 管理人名称,模糊查询
    #     company_ids: Union[str, List[str]] = None, # 排排网管理人id批量查询
    # ):
    #     """
    #     管理人大事记
    #     pvn_cm_company_grow_statis
    #     """
    #     t_company_grow_history = self.db.tables['smppw.pvn_cm_company_grow_statis']

    #     if isinstance(company_ids, str):
    #         company_ids = [company_ids]

    #     stmt = select(
    #         t_company_grow_history
    #     )

    #     if company_name is not None:
    #         stmt = stmt.where(
    #             t_company_grow_history.c.company_name.like(f'%{company_name}%'))

    #     if company_ids is not None:
    #         stmt = stmt.where(
    #             t_company_grow_history.c.company_id.in_(company_ids))

    #     return pd.read_sql(stmt, self.conn, index_col="company_id")

    def get_all_fund(
        self,
        types=["私募证券"],
        date=None,
    ):
        fund_type = [FUNDTYPE_PPW_MAP[type_name] for type_name in types]

        all_fund = self._get_fund_info(fund_type=fund_type, est_start=date)

        fields = [
            "fund_name",
            "fund_short_name",
            "fund_type",
            "inception_date",
            "register_date",
        ]

        return all_fund[fields]

    def get_fund(
        self,
        names: Union[str, List[str]] = None,
        reg_ids: Union[str, List[str]] = None,
        est_start: Union[str, pd.Timestamp] = None,
        est_end: Union[str, pd.Timestamp] = None,
        min_nvnum: int = None,
        nv_start: Union[str, pd.Timestamp] = None,
        nv_end: Union[str, pd.Timestamp] = None,
        strategies: Union[str, List[str]] = None,
        second_strategies: Union[str, List[str]] = None,
        third_strategies: Union[str, List[str]] = None,
        companys: Union[str, List[str]] = None,
        managers: Union[str, List[str]] = None,
    ):
        """
        筛选产品,根据

        名称
        备案编码

        成立日期区间

        净值数量
        净值区间

        产品策略类型
        所属管理人名称
        运行状态
        基金经理

        return:
            fund id列表
        """
        _fund_info = self._get_fund_info()
        _fund_strategy = self._get_fund_strategy()
        _company_info = self._get_company_info()

        fund_index = _fund_info.index
        # 名称过滤
        if names is not None:
            if isinstance(names, str):
                names = [names]
            masks = []
            for name in names:
                masks.append(_fund_info.fund_name.str.contains(name))
            fundname_mask = pd.concat(masks, axis=1).any(axis=1)

            fundname_filtered_index = fundname_mask.index[fundname_mask]
            fund_index = fund_index.join(fundname_filtered_index, how="inner")

            # fund_ids = fund_ids.join(id_by_names,how="inner")

        if reg_ids is not None:
            mask_id = _fund_info.register_number.isin(reg_ids)
            id_filtered_index = mask_id.index[mask_id]
            fund_index = fund_index.join(id_filtered_index, how="inner")

        if est_start is not None:
            mask_est_s = _fund_info.inception_date >= est_start
            est_s_filtered_index = mask_est_s.index[mask_est_s]
            fund_index = fund_index.join(est_s_filtered_index, how="inner")

        if est_end is not None:
            mask_est_e = _fund_info.inception_date <= est_end
            est_e_filtered_index = mask_est_e.index[mask_est_e]
            fund_index = fund_index.join(est_e_filtered_index, how="inner")

        if strategies is not None:
            if isinstance(strategies, str):
                strategies = [strategies]
            query_args = []
            for s in strategies:
                query_args.append(STRATEGY_PPW_MAP.get(s))
            strategies_mask = _fund_strategy.first_strategy.isin(query_args)
            strategies_filtered_index = strategies_mask.index[strategies_mask]
            fund_index = fund_index.join(strategies_filtered_index, how="inner")

        if second_strategies is not None:
            if isinstance(second_strategies, str):
                second_strategies = [second_strategies]
            query_args = []
            for s in second_strategies:
                query_args.append(SECOND_STRATEGY_PPW_MAP.get(s))
            second_strategies_mask = _fund_strategy.second_strategy.isin(query_args)
            second_strategies_filtered_index = second_strategies_mask.index[
                second_strategies_mask
            ]
            fund_index = fund_index.join(second_strategies_filtered_index, how="inner")

        if third_strategies is not None:
            if isinstance(third_strategies, str):
                third_strategies = [third_strategies]
            query_args = []
            for s in third_strategies:
                query_args.append(THIRD_STRATEGY_PPW_MAP.get(s))
            third_strategies_mask = _fund_strategy.third_strategy.isin(query_args)
            third_strategies_filtered_index = third_strategies_mask.index[
                third_strategies_mask
            ]
            fund_index = fund_index.join(third_strategies_filtered_index, how="inner")

        if companys is not None:
            if isinstance(companys, str):
                companys = [companys]
            masks = []
            for comp in companys:
                masks.append(_company_info.company_name.str.contains(comp))
            companyname_mask = pd.concat(masks, axis=1).any(axis=1)
            companyname_filtered_index = companyname_mask.index[companyname_mask]
            fund_index = fund_index.join(companyname_filtered_index, how="inner")

        return fund_index

    def get_fund_info(fund_ids: Union[str, List[str]], fields):
        # TODO:待完善具体查询的产品信息(要素、费率、策略、基金经理等)
        pass

    def get_company(
        self,
        names: Union[str, List[str]] = None,
        reg_ids: Union[str, List[str]] = None,
        province: Union[str, List[str]] = None,
        city: Union[str, List[str]] = None,
        est_start: Union[str, pd.Timestamp] = None,
        est_end: Union[str, pd.Timestamp] = None,
        aum_min: int = None,
        aum_max: int = None,
    ):
        """
        筛选管理人,根据

        名称
        协会登记编码
        所在地区(省,市)

        成立日期区间

        管理规模区间
        管理产品数量
        管理涉及的策略类型
        所属产品名称

        return:
            company id列表
        """
        _company_info = self._get_company_info()

        company_index = _company_info.index
        # 名称过滤
        if names is not None:
            if isinstance(names, str):
                names = [names]
            masks = []
            for name in names:
                masks.append(_company_info.company_name.str.contains(name))
            companyname_mask = pd.concat(masks, axis=1).any(axis=1)

            companyname_filtered_index = companyname_mask.index[companyname_mask]
            company_index = company_index.join(companyname_filtered_index, how="inner")

        if reg_ids is not None:
            mask_id = _company_info.register_number.isin(reg_ids)
            id_filtered_index = mask_id.index[mask_id]
            company_index = company_index.join(id_filtered_index, how="inner")

        return company_index

    def get_company_basic_info(
        self,
        company_name=None,
        company_ids=None,
        register_numbers=None,
    ):
        """
        根据id查询公司基础信息
        """
        company_info = self._get_company_info(
            company_name=company_name,
            register_numbers=register_numbers,
            company_ids=company_ids,
        )
        cols = {
            "company_name": "公司名称",
            "registered_capital": "注册资本",
            "paid_capital": "实缴资本",
            "establish_date": "成立日期",
            "register_date": "备案日期",
            "register_number": "备案编码",
            "is_member": "是否会员",
            "join_date": "入会时间",
            "member_type": "会员类型",
            "employee_cnts": "员工人数",
        }
        return company_info[cols.keys()].rename(columns=cols)

    def get_qr_description(
        self,
        company_name=None,
        company_ids=None,
        register_numbers=None,
    ):
        reports = self._get_qr_report(
            company_ids=company_ids,
            company_name=company_name,
            register_numbers=register_numbers,
        )

        most_recent_report_idx = reports.groupby("company_id")["report_date"].idxmax()

        summary = self._get_qr_summary(most_recent_report_idx)

        def desc_mertics(subdf):
            metrics = {}

            metrics["公司概况"] = subdf.query(
                "second_root_name=='公司概况'"
            ).node_name_content.squeeze()
            metrics["股东情况"] = subdf.query(
                "second_root_name=='股东情况'"
            ).node_name_content.squeeze()
            metrics["组织架构"] = subdf.query(
                "second_root_name=='组织架构'"
            ).node_name_content.squeeze()
            metrics["核心人员背景"] = subdf.query(
                "second_root_name=='核心人员背景'"
            ).node_name_content.squeeze()
            metrics["其他人员背景"] = subdf.query(
                "second_root_name=='其他人员背景'"
            ).node_name_content.squeeze()

            metrics["策略类型"] = subdf.query(
                "node_name=='策略类型'"
            ).node_name_content.squeeze()
            metrics["配置逻辑"] = subdf.query(
                "node_name=='配置逻辑'"
            ).node_name_content.squeeze()
            metrics["持仓特征"] = subdf.query(
                "node_name=='持仓特征'"
            ).node_name_content.squeeze()
            metrics["交易风格"] = subdf.query(
                "node_name=='交易风格'"
            ).node_name_content.squeeze()

            metrics["风控手段"] = subdf.query(
                "second_root_name=='风控手段'"
            ).node_name_content.squeeze()
            metrics["风控效果"] = subdf.query(
                "second_root_name=='风控效果'"
            ).node_name_content.squeeze()

            metrics["管理规模"] = subdf.query(
                "second_root_name=='管理规模'"
            ).node_name_content.squeeze()
            metrics["产品概述"] = subdf.query(
                "second_root_name=='产品概述'"
            ).node_name_content.squeeze()
            metrics["代表产品"] = subdf.query(
                "second_root_name=='代表产品'"
            ).node_name_content.squeeze()
            metrics["其他产品"] = subdf.query(
                "second_root_name=='其他产品'"
            ).node_name_content.squeeze()

            metrics["结论"] = subdf.query("root_name=='结论'").node_name_content.squeeze()
            return pd.Series(metrics)

        metrics = summary.groupby("qr_id").apply(desc_mertics)
        metrics["company_id"] = reports.loc[metrics.index].company_id
        metrics.set_index("company_id", drop=True, inplace=True)
        return metrics
