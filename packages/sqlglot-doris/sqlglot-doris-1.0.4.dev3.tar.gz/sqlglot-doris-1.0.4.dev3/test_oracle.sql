select to_char(trunc(sysdate), 'yyyymm'),
       nvl(b.countycode, a.countycode),
       nvl(b.countyname, a.countyname),
       nvl(b.COMPANYCLASSNAME, a.areaname1),
       nvl(b.CLASSTYPE1, a.classtype),
       nvl(b.SIGNPREMIUM_day, 0),
       nvl(b.SIGNPREMIUM_month, 0),
       nvl(b.SIGNPREMIUM_year, 0),
       nvl(b.SIGNPREMIUM_dayls, 0),
       nvl(b.SIGNPREMIUM_monthls, 0),
       nvl(b.SIGNPREMIUM_last, 0),
       nvl(b.UWPREMIUM_day, 0),
       nvl(b.UWPREMIUM_month, 0),
       nvl(b.UWPREMIUM_year, 0),
       nvl(b.UWPREMIUM_dayls, 0),
       nvl(b.UWPREMIUM_monthls, 0),
       nvl(b.UWPREMIUM_last, 0),
       nvl(b.SIGNPREMIUM_day, 0) - nvl(c.amountreceivablenotax_day, 0) as PREMIUMACC_day,
       nvl(b.SIGNPREMIUM_month, 0) - nvl(c.amountreceivablenotax_month, 0) as PREMIUMACC_month,
       case
         when nvl(b.CLASSTYPE1, a.classtype) = '机动车辆保险类' then
          case
            when nvl(b.SIGNPREMIUM_year, 0) <=
                 nvl(a.classpremium_lj * 1.1, 0) * 10000 then
             nvl(b.SIGNPREMIUM_year, 0) - nvl(c.amountreceivablenotax_year, 0)
            else
             nvl(a.classpremium_lj * 1.1, 0) * 10000 -
             nvl(c.amountreceivablenotax_year, 0)
          end
         else
          nvl(b.SIGNPREMIUM_year, 0) - nvl(c.amountreceivablenotax_year, 0)
       end as PREMIUMACC_year, --当年考核保费，车险部分 签单保费和指标值 取小 减去 应收未收
       nvl(b.SIGNPREMIUM_dayls, 0) - nvl(c.amountreceivablenotax_dayls, 0) as PREMIUMACC_dayls,
       nvl(b.SIGNPREMIUM_monthls, 0) -
       nvl(c.amountreceivablenotax_monthls, 0) as PREMIUMACC_monthls,
       nvl(b.SIGNPREMIUM_last, 0) - nvl(c.amountreceivablenotax_last, 0) as PREMIUMACC_last,
       nvl(a.classpremium_lj, 0),
       nvl(a.classpremium_y, 0),
       nvl(d.LIQUIDATETARGETDN, 0),
       nvl(d.LIQUIDATEAMOUNTDN, 0),
       nvl(d.AMOUNTRECEIVABLEDN, 0),
       nvl(d.LIQUIDATETARGETLS, 0),
       nvl(d.LIQUIDATEAMOUNTLS, 0),
       nvl(d.AMOUNTRECEIVABLELS, 0)
  from (select a.countycode,
               A.countyname,
               case
                 when a.classcode in ('31', '32') then
                  '农险'
                 when a.classcode in ('26') then
                  '健康险'
                 when a.classcode in ('22') then
                  '信用保证保险'
                 else
                  '非农商险'
               end areaname1,
               a.classtype,
               sum(a.classpremium) classpremium_y,
               sum(nvl(case
                         when statmonth <= to_char(sysdate, 'yyyymm') then
                          classpremium
                       end,
                       0)) classpremium_lj, --当年到当月累计计划保费
               sum(nvl(case
                         when statmonth = to_char(sysdate, 'yyyymm') then
                          classpremium
                       end,
                       0)) classpremium_dy, --当月计划保费
               sum(nvl(case
                         when statmonth < to_char(sysdate, 'yyyymm') then
                          classpremium
                       end,
                       0)) classpremium_ly --当年历史月份计划保费
          from (select a.statmonth,
                       a.countycode,
                       case
                         when a.risktype2 in ('夏粮', '秋粮', '其他') and
                              a.risktype1 = '种植险' then
                          '31'
                         when a.risktype2 in ('育肥猪', '其他') then
                          '32'
                         when a.risktype2 in ('意外险') then
                          '27'
                         when a.risktype2 in ('健康险') then
                          '26'
                         when a.risktype2 in ('商车', '交强') then
                          '05'
                         when a.risktype2 in ('企财险') then
                          '01'
                         when a.risktype2 in ('家财险') then
                          '03'
                         when a.risktype2 in ('责任险') then
                          '15'
                         when a.risktype2 in ('工程险') then
                          '08'
                         when a.risktype2 in
                              ('融资类保证保险', '非融资类保证保险') then
                          '22'
                         when a.risktype2 in ('货运险') then
                          '09'
                         else
                          '20'
                       end classcode,
                       sum(a.classpremium) classpremium,
                       case
                         when a.risktype2 in ('夏粮', '秋粮', '其他') and
                              a.risktype1 = '种植险' then
                          '种植保险类'
                         when a.risktype2 in ('育肥猪', '其他') then
                          '养殖保险类'
                         when a.risktype2 in ('意外险') then
                          '意外险类'
                         when a.risktype3 in ('经办类', '政策性') then
                          '保障政策性'
                         when a.risktype3 = '非政策性' then
                          '保障非政策性'
                         when a.risktype2 in ('商车', '交强') then
                          '机动车辆保险类'
                         when a.risktype2 in ('企财险') then
                          '企业财产保险类'
                         when a.risktype2 in ('家财险') then
                          '普通家财保险类'
                         when a.risktype2 in ('责任险') then
                          '责任保险类'
                         when a.risktype2 in ('工程险') then
                          '工程一切险类'
                         when a.risktype2 in ('融资类保证保险') then
                          '融资类'
                         when a.risktype2 in ('非融资类保证保险') then
                          '非融资类'
                         when a.risktype2 in ('货运险') then
                          '货运险'
                         else
                          '综合险类'
                       end classtype,
                       a.countyname
                  from WEB_BS_CLASSPLANPREMIUM a
                 where a.hierarchy = '3'
                   and substr(statmonth, 1, 4) =
                       to_char(trunc(sysdate), 'yyyy')
                 group by case
                            when a.risktype2 in ('夏粮', '秋粮', '其他') and
                                 a.risktype1 = '种植险' then
                             '31'
                            when a.risktype2 in ('育肥猪', '其他') then
                             '32'
                            when a.risktype2 in ('意外险') then
                             '27'
                            when a.risktype2 in ('健康险') then
                             '26'
                            when a.risktype2 in ('商车', '交强') then
                             '05'
                            when a.risktype2 in ('企财险') then
                             '01'
                            when a.risktype2 in ('家财险') then
                             '03'
                            when a.risktype2 in ('责任险') then
                             '15'
                            when a.risktype2 in ('工程险') then
                             '08'
                            when a.risktype2 in
                                 ('融资类保证保险', '非融资类保证保险') then
                             '22'
                            when a.risktype2 in ('货运险') then
                             '09'
                            else
                             '20'
                          end,
                          case
                            when a.risktype2 in ('夏粮', '秋粮', '其他') and
                                 a.risktype1 = '种植险' then
                             '种植保险类'
                            when a.risktype2 in ('育肥猪', '其他') then
                             '养殖保险类'
                            when a.risktype2 in ('意外险') then
                             '意外险类'
                            when a.risktype3 in ('经办类', '政策性') then
                             '保障政策性'
                            when a.risktype3 = '非政策性' then
                             '保障非政策性'
                            when a.risktype2 in ('商车', '交强') then
                             '机动车辆保险类'
                            when a.risktype2 in ('企财险') then
                             '企业财产保险类'
                            when a.risktype2 in ('家财险') then
                             '普通家财保险类'
                            when a.risktype2 in ('责任险') then
                             '责任保险类'
                            when a.risktype2 in ('工程险') then
                             '工程一切险类'
                            when a.risktype2 in ('融资类保证保险') then
                             '融资类'
                            when a.risktype2 in ('非融资类保证保险') then
                             '非融资类'
                            when a.risktype2 in ('货运险') then
                             '货运险'
                            else
                             '综合险类'
                          end,
                          a.statmonth,
                          a.countycode,
                          a.countyname) a
         where substr(statmonth, 1, 4) = to_char(sysdate, 'yyyy')
         group by case
                    when a.classcode in ('31', '32') then
                     '农险'
                    when a.classcode in ('26') then
                     '健康险'
                    when a.classcode in ('22') then
                     '信用保证保险'
                    else
                     '非农商险'
                  end,
                  a.classtype,
                  a.countycode,
                  A.countyname) a
  full join (select
              to_char(trunc(sysdate), 'yyyymm'),
              nvl(c.countycode, b.countycode) countycode,
              nvl(c.countyname, b.countyname) countyname,
              case
                when a.classcode in ('31', '32') then
                 '农险'
                when a.classcode in ('26') then
                 '健康险'
                when a.classcode in ('22') then
                 '信用保证保险'
                else
                 '非农商险'
              end COMPANYCLASSNAME,
              case
                when a.classcode = '22' then
                 (case
                   when a.riskcode in ('2213', '2202', '2212', '2227', '2215') then
                    '融资类'
                   else
                    '非融资类'
                 end)
                when a.classcode = '26' then
                 (case
                   when a.riskcode in ('2609',
                                       '2614',
                                       '2615',
                                       '2635',
                                       '2636',
                                       '2637',
                                       '2639',
                                       '2640') or
                        (a2.appliidentifytype = '64' and
                        a2.appliidentifynumber like '1%') or
                        (a1.insuredidentifytype = '64' and
                        a1.insuredidentifynumber like '1%') then
                    '保障政策性'
                   else
                    '保障非政策性'
                 end)
                else
                 decode(a.classname,
                        '国内货物运输保险类',
                        '货运险',
                        '货运预约协议保险类',
                        '货运险',
                        a.classname)
              end CLASSTYPE1,
              nvl(sum(case
                        when a.statdate = trunc(trunc(sysdate)) then
                         notaxpremium
                      end),
                  0) as SIGNPREMIUM_day, --当日保费收入
              nvl(sum(case
                        when a.statdate between trunc(trunc(sysdate), 'MM') and
                             trunc(trunc(sysdate)) then
                         notaxpremium
                      end),
                  0) as SIGNPREMIUM_month, --当月
              nvl(sum(case
                        when a.statdate between trunc(trunc(sysdate), 'YYYY') and
                             trunc(trunc(sysdate)) then
                         notaxpremium
                      end),
                  0) as SIGNPREMIUM_year, --当年
              nvl(sum(case
                        when a.statdate >= trunc(trunc(sysdate), 'YYYY') and
                             a.statdate < trunc(trunc(sysdate), 'MM') then
                         notaxpremium
                      end),
                  0) as SIGNPREMIUM_ly, --当年历史月份签单保费
              nvl(sum(case
                        when a.statdate = add_months(trunc(trunc(sysdate)), -12) then
                         notaxpremium
                      end),
                  0) as SIGNPREMIUM_dayls, --去年当日保费收入
              nvl(sum(case
                        when a.statdate between
                             add_months(trunc(trunc(sysdate), 'MM'), -12) and
                             add_months(trunc(trunc(sysdate)), -12) then
                         notaxpremium
                      end),
                  0) as SIGNPREMIUM_monthls, --去年当月

              nvl(sum(case
                        when a.statdate between
                             add_months(trunc(trunc(sysdate), 'YYYY'), -12) and
                             add_months(trunc(trunc(sysdate)), -12) then
                         notaxpremium
                      end),
                  0) as SIGNPREMIUM_last --去年同期
             ,
              nvl(sum(case
                        when a.singdate = trunc(trunc(sysdate)) then
                         notaxpremium
                      end),
                  0) as UWPREMIUM_day, --当日核单收入

              nvl(sum(case
                        when a.singdate between trunc(trunc(sysdate), 'MM') and
                             trunc(trunc(sysdate)) then
                         notaxpremium
                      end),
                  0) as UWPREMIUM_month, --当月
              nvl(sum(case
                        when a.singdate between trunc(trunc(sysdate), 'YYYY') and
                             trunc(trunc(sysdate)) then
                         notaxpremium
                      end),
                  0) as UWPREMIUM_year, --当年
              nvl(sum(case
                        when a.singdate = add_months(trunc(trunc(sysdate)), -12) then
                         notaxpremium
                      end),
                  0) as UWPREMIUM_dayls, --去年当日核单收入

              nvl(sum(case
                        when a.singdate between
                             add_months(trunc(trunc(sysdate), 'MM'), -12) and
                             add_months(trunc(trunc(sysdate)), -12) then
                         notaxpremium
                      end),
                  0) as UWPREMIUM_monthls, --去年当月
              nvl(sum(case
                        when a.singdate between
                             add_months(trunc(trunc(sysdate), 'YYYY'), -12) and
                             add_months(trunc(trunc(sysdate)), -12) then
                         notaxpremium
                      end),
                  0) as UWPREMIUM_last --去年同期
               from (select a.POLICYNO endorseno,
                            a.POLICYNO,
                            a.comcode,
                            a.teamcode,
                            a.classcode,
                            e.classname,
                            a.riskcode,
                            a.operationensure,
                            trunc(a.validcountdate, 'dd') as statdate,
                            decode(a.isseefeeflag,
                                   '1',
                                   trunc(greatest(a.underwriteenddate,
                                                  a.paydate),
                                         'dd'),
                                   trunc(a.underwriteenddate, 'dd')) as singdate,
                            sum(a.sumnotaxpremium *
                                decode(a.coinsflag,
                                       0,
                                       1,
                                       decode(c.coinsrate,
                                              null,
                                              100,
                                              c.coinsrate) / 100)) as notaxpremium --原币保费收入

                       from zyic.prpcmainorigin a
                      inner join zyic.prpcmain d
                         on a.POLICYNO = d.POLICYNO
                       left join zyic.prpccoinsorigin c
                         on a.POLICYNO = c.POLICYNO
                       left join zyic.prpdclass e
                         on a.classcode = e.classcode
                      where (c.coinstype = '1' or c.coinstype is null)
                        and a.underwriteflag in ('1', '3')
                        and a.underwriteenddate is not null
                        and substr(a.othflag, 8, 1) != 'N'
                        and substr(a.othflag, 7, 1) != 'N'
                      group by a.comcode,
                               a.POLICYNO,
                               a.teamcode,
                               a.classcode,
                               e.classname,
                               a.riskcode,
                               a.operationensure,
                               trunc(a.validcountdate, 'dd'),
                               decode(a.isseefeeflag,
                                      '1',
                                      trunc(greatest(a.underwriteenddate,
                                                     a.paydate),
                                            'dd'),
                                      trunc(a.underwriteenddate, 'dd'))
                     union all
                     select a.endorseno,
                            a.POLICYNO,
                            a.comcode,
                            c.teamcode,
                            a.classcode,
                            e.classname,
                            a.riskcode,
                            c.operationensure,
                            trunc(a.validcountdate, 'dd') as statdate,
                            decode(a.isseefeeflag,
                                   '1',
                                   trunc(greatest(a.underwriteenddate,
                                                  a.paydate),
                                         'dd'),
                                   trunc(a.underwriteenddate, 'dd')) singdate,
                            sum(c.chgnotaxpremium *
                                decode(c.coinsflag,
                                       0,
                                       1,
                                       decode(d.coinsrate,
                                              null,
                                              100,
                                              d.coinsrate) / 100)) as notaxpremium --原币保费收入

                       from zyic.prpphead a
                      inner join zyic.prppmain c
                         on a.endorseno = c.endorseno
                       left join zyic.prpccoins d
                         on a.POLICYNO = d.POLICYNO
                       left join zyic.prpdclass e
                         on a.classcode = e.classcode
                      where (d.coinstype = '1' or d.coinstype is null)
                        and a.underwriteflag in ('1', '3')
                        and substr(c.othflag, 8, 1) != 'N'
                        and substr(c.othflag, 7, 1) != 'N'
                      group by a.comcode,
                               a.endorseno,
                               a.POLICYNO,
                               c.teamcode,
                               a.classcode,
                               e.classname,
                               a.riskcode,
                               c.operationensure,
                               trunc(a.validcountdate, 'dd'),
                               decode(a.isseefeeflag,
                                      '1',
                                      trunc(greatest(a.underwriteenddate,
                                                     a.paydate),
                                            'dd'),
                                      trunc(a.underwriteenddate, 'dd'))) a
               left join cd_levelcompany b
                 on a.comcode = b.comcode
               left join cd_teamcompany c
                 on a.teamcode = c.teamcode

               left join (select POLICYNO,
                                max(identifytype) insuredidentifytype, --投保人证件类型
                                max(identifynumber) insuredidentifynumber --投保人证件号码
                           from zyic.prpcinsured
                          where insuredflag = '1'
                          group by POLICYNO) a1
                 on a.POLICYNO = a1.POLICYNO
               left join (select POLICYNO,
                                max(identifytype) appliidentifytype, --投保人证件类型
                                max(identifynumber) appliidentifynumber --投保人证件号码
                           from zyic.prpcinsured
                          where insuredflag = '2'
                          group by POLICYNO) a2
                 on a.POLICYNO = a2.POLICYNO

              group by to_char(trunc(sysdate), 'yyyymm'),
                       nvl(c.countycode, b.countycode),
                       nvl(c.countyname, b.countyname),
                       case
                         when a.classcode in ('31', '32') then
                          '农险'
                         when a.classcode in ('26') then
                          '健康险'
                         when a.classcode in ('22') then
                          '信用保证保险'
                         else
                          '非农商险'
                       end,
                       case
                         when a.classcode = '22' then
                          (case
                            when a.riskcode in
                                 ('2213', '2202', '2212', '2227', '2215') then
                             '融资类'
                            else
                             '非融资类'
                          end)
                         when a.classcode = '26' then
                          (case
                            when a.riskcode in ('2609',
                                                '2614',
                                                '2615',
                                                '2635',
                                                '2636',
                                                '2637',
                                                '2639',
                                                '2640') or
                                 (a2.appliidentifytype = '64' and
                                 a2.appliidentifynumber like '1%') or
                                 (a1.insuredidentifytype = '64' and
                                 a1.insuredidentifynumber like '1%') then
                             '保障政策性'
                            else
                             '保障非政策性'
                          end)
                         else
                          decode(a.classname,
                                 '国内货物运输保险类',
                                 '货运险',
                                 '货运预约协议保险类',
                                 '货运险',
                                 a.classname)
                       end) b
    on nvl(a.countycode, '0') = nvl(b.countycode, '0')
   and nvl(a.classtype, '0') = nvl(b.CLASSTYPE1, '0')

  left join (select /*+ parallel(8) */
              to_char(trunc(sysdate), 'yyyymm'),
              nvl(c.countycode, b.countycode) countycode,
              nvl(c.countyname, b.countyname) countyname,
              case
                when a.classcode in ('31', '32') then
                 '农险'
                when a.classcode in ('26') then
                 '健康险'
                when a.classcode in ('22') then
                 '信用保证保险'
                else
                 '非农商险'
              end COMPANYCLASSNAME,
              case
                when a.classcode = '22' then
                 (case
                   when a.riskcode in ('2213', '2202', '2212', '2227', '2215') then
                    '融资类'
                   else
                    '非融资类'
                 end)
                when a.classcode = '26' then
                 (case
                   when a.riskcode in ('2609',
                                       '2614',
                                       '2615',
                                       '2635',
                                       '2636',
                                       '2637',
                                       '2639',
                                       '2640') or
                        (a.APPLIIDENTIFYTYPE = '64' and
                        a.APPLIIDENTIFYNUMBER like '1%') or
                        (a.INSUREDIDENTIFYTYPE = '64' and
                        a.INSUREDIDENTIFYNUMBER like '1%') then
                    '保障政策性'
                   else
                    '保障非政策性'
                 end)
                else
                 decode(d.classname,
                        '国内货物运输保险类',
                        '货运险',
                        '货运预约协议保险类',
                        '货运险',
                        d.classname)
              end CLASSTYPE1,
              0 as amountreceivablenotax_day, --当日应清未清
              SUM(case
                    when x.liquidatestage between trunc(trunc(sysdate), 'MM') and
                         trunc(trunc(sysdate), 'dd') then
                     X.Amountreceivable
                    else
                     0
                  end) as amountreceivablenotax_month, --当月应清未清
              SUM(case
                    when x.liquidatestage between trunc(trunc(sysdate), 'YYYY') and
                         trunc(trunc(sysdate), 'dd') then
                     X.Amountreceivable
                    else
                     0
                  end) as amountreceivablenotax_year, --当年应清未清
              SUM(case
                    when trunc(x.liquidatestage) >= trunc(trunc(sysdate), 'YYYY') and
                         trunc(x.liquidatestage) < trunc(trunc(sysdate), 'MM') then
                     X.Amountreceivable
                    else
                     0
                  end) as amountreceivablenotax_ly, --当年历史月份应清未清
              0 as amountreceivablenotax_dayls, -- 去年当日应清未清
              SUM(case
                    when x.liquidatestage between
                         add_months(trunc(trunc(sysdate), 'MM'), -12) and
                         add_months(trunc(trunc(sysdate), 'dd'), -12) then
                     X.Amountreceivable
                    else
                     0
                  end) as amountreceivablenotax_monthls, --去年当月应清未清
              SUM(case
                    when x.liquidatestage between
                         add_months(trunc(trunc(sysdate), 'YYYY'), -12) and
                         add_months(trunc(trunc(sysdate)), -12) then
                     X.Amountreceivable
                    else
                     0
                  end) as amountreceivablenotax_last --去年同期
               from mid_cb_dim_all a
              inner join web_cb_qd_receivable_all x
                 on nvl(x.ENDORSENO, x.POLICYNO) = a.ENDORSEQNO
                and x.closeddate = trunc(sysdate) - 1
               left join MID_CB_DIM_HEALTH e
                 on e.POLICYNO = a.POLICYNO
                and e.ENDORSEQNO = a.ENDORSEQNO
               left join cd_levelcompany b
                 on a.comcode = b.comcode
               left join cd_teamcompany c
                 on a.teamcode = c.teamcode
               left join zyic.prpdclass D
                 on D.Classcode = A.Classcode
              group by to_char(trunc(sysdate), 'yyyymm'),
                       nvl(c.countycode, b.countycode),
                       nvl(c.countyname, b.countyname),
                       case
                         when a.classcode in ('31', '32') then
                          '农险'
                         when a.classcode in ('26') then
                          '健康险'
                         when a.classcode in ('22') then
                          '信用保证保险'
                         else
                          '非农商险'
                       end,
                       case
                         when a.classcode = '22' then
                          (case
                            when a.riskcode in
                                 ('2213', '2202', '2212', '2227', '2215') then
                             '融资类'
                            else
                             '非融资类'
                          end)
                         when a.classcode = '26' then
                          (case
                            when a.riskcode in ('2609',
                                                '2614',
                                                '2615',
                                                '2635',
                                                '2636',
                                                '2637',
                                                '2639',
                                                '2640') or
                                 (a.APPLIIDENTIFYTYPE = '64' and
                                 a.APPLIIDENTIFYNUMBER like '1%') or
                                 (a.INSUREDIDENTIFYTYPE = '64' and
                                 a.INSUREDIDENTIFYNUMBER like '1%') then
                             '保障政策性'
                            else
                             '保障非政策性'
                          end)
                         else
                          decode(d.classname,
                                 '国内货物运输保险类',
                                 '货运险',
                                 '货运预约协议保险类',
                                 '货运险',
                                 d.classname)
                       end) c
    on nvl(a.countycode, nvl(b.countycode, '0')) = nvl(c.countycode, '0')
   and nvl(a.classtype, nvl(b.CLASSTYPE1, '0')) = nvl(c.CLASSTYPE1, '0')
  left join (select a.countycode,
                    b.areaname,
                    case
                      when substr(a.riskcode, 1, 2) in ('31', '32') then
                       '农险'
                      when substr(a.riskcode, 1, 2) in ('26') then
                       '健康险'
                      when substr(a.riskcode, 1, 2) in ('22') then
                       '信用保证保险'
                      else
                       '非农商险'
                    end as classtype,
                    case
                      when g.classcode = '22' then
                       g.cropname
                      when g.classcode = '26' then
                       (case
                         when a.riskcode in ('2609',
                                             '2614',
                                             '2615',
                                             '2635',
                                             '2636',
                                             '2637',
                                             '2639',
                                             '2640') then
                          '保障政策性'
                         else
                          '保障非政策性'
                       end)
                      else
                       decode(g.classname,
                              '国内货物运输保险类',
                              '货运险',
                              '货运预约协议保险类',
                              '货运险',
                              g.classname)
                    end classtype1,
                    sum(case
                          when liquidatestage >= trunc(sysdate - 1, 'yyyy') and
                               liquidatestage <= trunc(sysdate) then
                           a.liquidatetarget
                        end) as LIQUIDATETARGETDN, --目标当年
                    sum(case
                          when liquidatestage >= trunc(sysdate - 1, 'yyyy') and
                               liquidatestage <= trunc(sysdate) then
                           a.liquidateamount
                        end) as LIQUIDATEAMOUNTDN, --已清当年
                    sum(case
                          when liquidatestage >= trunc(sysdate - 1, 'yyyy') and
                               liquidatestage <= trunc(sysdate) then
                           a.amountreceivable
                        end) as AMOUNTRECEIVABLEDN, -- 未清当年
                    sum(case
                          when liquidatestage < trunc(sysdate - 1, 'yyyy') then
                           a.liquidatetarget
                        end) as LIQUIDATETARGETLS, --目标去年
                    sum(case
                          when liquidatestage < trunc(sysdate - 1, 'yyyy') then
                           a.liquidateamount
                        end) as LIQUIDATEAMOUNTLS, --已清去年
                    sum(case
                          when liquidatestage < trunc(sysdate - 1, 'yyyy') then
                           a.amountreceivable
                        end) as AMOUNTRECEIVABLELS -- 未清去年
               from web_bs_move_sf a
              inner join cd_companyareas b
                 on a.countycode = b.areacode
              inner join cd_classrisk g
                 on a.riskcode = g.riskcode
              where a.closeddate = trunc(sysdate - 1)
                and NVL(isliquidatedf, '1') <> '0'
              group by a.countycode,
                       b.areaname,
                       case
                         when substr(a.riskcode, 1, 2) in ('31', '32') then
                          '农险'
                         when substr(a.riskcode, 1, 2) in ('26') then
                          '健康险'
                         when substr(a.riskcode, 1, 2) in ('22') then
                          '信用保证保险'
                         else
                          '非农商险'
                       end,
                       case
                         when g.classcode = '22' then
                          g.cropname
                         when g.classcode = '26' then
                          (case
                            when a.riskcode in ('2609',
                                                '2614',
                                                '2615',
                                                '2635',
                                                '2636',
                                                '2637',
                                                '2639',
                                                '2640') then
                             '保障政策性'
                            else
                             '保障非政策性'
                          end)
                         else
                          decode(g.classname,
                                 '国内货物运输保险类',
                                 '货运险',
                                 '货运预约协议保险类',
                                 '货运险',
                                 g.classname)
                       end) d
    on nvl(d.countycode, '0') = nvl(a.countycode, nvl(b.countycode, '0'))
   and nvl(d.CLASSTYPE1, '0') = nvl(a.classtype, nvl(b.CLASSTYPE1, '0'));